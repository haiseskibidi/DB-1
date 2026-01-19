from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc
from typing import List, Optional
import sys
sys.path.append('..')

from . import models, schemas
from .database import get_db, init_db
from .importer import run_import

app = FastAPI(
    title="Culinary Aggregator API",
    description="API for recipes from RussianFood, Povarenok, 1000.menu",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()
    db = next(get_db())
    if db.query(models.Recipe).count() == 0:
        print("Database is empty. Importing data...")
        run_import()
    else:
        print("Database already populated.")


@app.get("/")
def root():
    return {
        "message": "Culinary Aggregator API",
        "docs": "/docs",
        "endpoints": {
            "search": "/api/search",
            "recipe": "/api/recipes/{id}",
            "stats": "/api/stats"
        }
    }


@app.get("/api/search", response_model=dict)
def search_recipes(
    q: Optional[str] = Query(None, description="Search by title/desc"),
    category: Optional[str] = Query(None, description="Category (Soup, Salad)"),
    ingredient: Optional[str] = Query(None, description="Ingredient"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)
    
    if q:
        q_lower = q.lower()
        search_filter = or_(
            func.lower(models.Recipe.title).contains(q_lower),
            func.lower(models.Recipe.description).contains(q_lower)
        )
        query = query.filter(search_filter)
    
    if category:
        query = query.filter(models.Recipe.category.like(f"%{category}%"))
    
    if ingredient:
        query = query.join(models.Ingredient).filter(
            models.Ingredient.name.like(f"%{ingredient}%")
        )
    
    total = query.count()
    
    recipes = query.order_by(desc(models.Recipe.created_at))\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    
    results = []
    for r in recipes:
        results.append({
            "id": r.id,
            "title": r.title,
            "category": r.category,
            "cooking_time": r.cooking_time,
            "difficulty": r.difficulty,
            "description": r.description[:150] + "..." if r.description else "",
            "source_count": len(r.sources)
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "results": results
    }


@app.get("/api/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.get("/api/stats", response_model=schemas.StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_recipes = db.query(models.Recipe).count()
    total_categories = db.query(models.Recipe.category).distinct().count()
    
    sources = db.query(
        models.RecipeSource.source_name,
        func.count(models.RecipeSource.id).label('count')
    ).group_by(models.RecipeSource.source_name).all()
    
    top_categories = db.query(
        models.Recipe.category,
        func.count(models.Recipe.id).label('count')
    ).group_by(models.Recipe.category)\
        .order_by(desc('count')).limit(5).all()
        
    top_ingredients = db.query(
        models.Ingredient.name,
        func.count(models.Ingredient.id).label('count')
    ).group_by(models.Ingredient.name)\
        .order_by(desc('count')).limit(10).all()
    
    return {
        "total_recipes": total_recipes,
        "total_categories": total_categories,
        "recipes_by_source": {s.source_name: s.count for s in sources},
        "top_categories": [{"category": c.category, "count": c.count} for c in top_categories],
        "top_ingredients": [{"ingredient": i.name, "count": i.count} for i in top_ingredients]
    }
    
@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(models.Recipe.category).distinct().all()
    return [c.category for c in cats if c.category]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)