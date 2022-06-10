from typing import List

from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from models.db.recipe_items import RecipeItem
from models.db.recipe import Recipe
from models.db.tags import Tags

PydanticRecipeItem = sqlalchemy_to_pydantic(RecipeItem)
PydanticTags = sqlalchemy_to_pydantic(Tags)
PydanticRecipe = sqlalchemy_to_pydantic(Recipe)
