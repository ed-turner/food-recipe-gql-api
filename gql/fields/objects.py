import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from gql.fields.base import AsyncSQLAlchemyObjectType
from models.db.recipe import Recipe
from models.db.recipe_items import RecipeItem
from models.db.tags import Tags


class RecipeObjectType(SQLAlchemyObjectType):
    class Meta:
        model = Recipe
        interfaces = (relay.Node,)


class TagObjectType(SQLAlchemyObjectType):
    class Meta:
        model = Tags
        interfaces = (relay.Node,)


class RecipeItemObjectType(SQLAlchemyObjectType):
    class Meta:
        model = RecipeItem
        interfaces = (relay.Node,)


RecipeObjectType.recipeTags = graphene.List(TagObjectType)
TagObjectType.taggedRecipes = graphene.List(RecipeObjectType)
