import json
import re
import os
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Recipe, RecipeSource, Ingredient
from rapidfuzz import fuzz

def normalize_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def find_duplicate(db, title):
    norm_title = normalize_text(title)
    
    exact = db.query(Recipe).filter(Recipe.title == title).first()
    if exact:
        return exact
        
    return None 

def import_recipes_from_file(json_file, source_name, db: Session):
    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        return

    print(f"\n[{source_name}] Loading from {json_file}...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
        return
    
    print(f"Found {len(data)} recipes")
    
    added_count = 0
    duplicate_count = 0
    
    for item in data:
        title = item.get('title')
        if not title:
            continue
        
        existing = db.query(Recipe).filter(Recipe.title == title).first()
        
        if existing:
            duplicate_count += 1
            src_exists = db.query(RecipeSource).filter_by(
                recipe_id=existing.id,
                source_name=source_name
            ).first()
            if not src_exists:
                db.add(RecipeSource(
                    recipe_id=existing.id,
                    source_name=source_name,
                    source_url=item.get('url', '')
                ))
        else:
            recipe = Recipe(
                title=title,
                category=item.get('category'),
                cooking_time=item.get('cooking_time'),
                difficulty=item.get('difficulty'),
                description=item.get('description'),
                image_url=item.get('image_url')
            )
            db.add(recipe)
            db.flush()
            
            db.add(RecipeSource(
                recipe_id=recipe.id,
                source_name=source_name,
                source_url=item.get('url', '')
            ))
            
            ing_text = item.get('ingredients', '')
            if ing_text:
                ingredients = [i.strip() for i in ing_text.split(',')]
                for ing in ingredients[:15]: 
                    if ing:
                        db.add(Ingredient(recipe_id=recipe.id, name=ing))
            
            added_count += 1
    
    db.commit()
    print(f"[{source_name}] Added: {added_count}, Duplicates: {duplicate_count}")

def run_import():
    db = SessionLocal()
    try:
        base_paths = ['/app/data', '../data', 'data']
        data_dir = None
        for p in base_paths:
            if os.path.exists(p) and os.path.isdir(p):
                data_dir = p
                break
        
        if not data_dir:
            print("Data directory not found.")
            return

        import_recipes_from_file(os.path.join(data_dir, 'russianfood_data.json'), 'russianfood.com', db)
        import_recipes_from_file(os.path.join(data_dir, 'povarenok_data.json'), 'povarenok.ru', db)
        import_recipes_from_file(os.path.join(data_dir, 'menu1000_data.json'), '1000.menu', db)
        
    finally:
        db.close()