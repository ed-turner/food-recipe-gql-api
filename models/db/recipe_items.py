
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class RecipeItem(Base):
    __tablename__ = 'recipe_item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    measureQuantity = Column(Float, nullable=False)
    measureUnit = Column(String, nullable=False)

    recipe = relationship('Recipe', uselist=False, lazy='bulk', back_populates="recipe_items")
    recipe_id = Column(ForeignKey('recipe.id'), nullable=False)

