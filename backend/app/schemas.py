from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IngredientBase(BaseModel):
    name: str

class Ingredient(IngredientBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class RecipeSourceBase(BaseModel):
    source_name: str
    source_url: str

class RecipeSource(RecipeSourceBase):
    id: int
    recipe_id: int
    parsed_at: datetime

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    title: str
    category: Optional[str] = None
    cooking_time: Optional[str] = None
    difficulty: Optional[str] = None
    description: Optional[str] = None

class Recipe(RecipeBase):
    id: int
    created_at: datetime
    sources: List[RecipeSource] = []
    ingredients: List[Ingredient] = []

    class Config:
        orm_mode = True

class StatsResponse(BaseModel):
    total_recipes: int
    total_categories: int
    recipes_by_source: dict
    top_categories: list
    top_ingredients: list