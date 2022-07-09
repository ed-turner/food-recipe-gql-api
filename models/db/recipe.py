from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .associations import recipe_tags_table


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    direction = Column(String)

    recipe_tags = relationship(
        'Tags',
        lazy='bulk',
        secondary=recipe_tags_table,
        back_populates="tagged_recipes",
    )

    recipe_items = relationship(
        'RecipeItem',
        lazy='bulk',
        back_populates="recipe",
        cascade="all, delete, delete-orphan"
    )

