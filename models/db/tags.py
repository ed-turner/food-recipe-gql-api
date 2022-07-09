from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .associations import recipe_tags_table


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    tagged_recipes = relationship('Recipe',
                                  lazy='bulk',
                                  secondary=recipe_tags_table,
                                  back_populates="recipe_tags")
