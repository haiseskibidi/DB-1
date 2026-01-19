from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True) 
    cooking_time = Column(String)         
    difficulty = Column(String)           
    description = Column(Text)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sources = relationship("RecipeSource", back_populates="recipe", cascade="all, delete-orphan")
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")

class RecipeSource(Base):
    __tablename__ = "recipe_sources"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    source_name = Column(String) 
    source_url = Column(String)
    parsed_at = Column(DateTime(timezone=True), server_default=func.now())

    recipe = relationship("Recipe", back_populates="sources")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    name = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")