from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from gql.v1.fields.base import SessionSQLAlchemyObjectType
from models.db.recipe import Recipe
from models.db.recipe_items import RecipeItem
from models.db.tags import Tags


class RecipeObjectType(SessionSQLAlchemyObjectType, SQLAlchemyObjectType):
    class Meta:
        model = Recipe
        interfaces = (relay.Node,)


class TagObjectType(SessionSQLAlchemyObjectType, SQLAlchemyObjectType):
    class Meta:
        model = Tags
        interfaces = (relay.Node,)


class RecipeItemObjectType(SessionSQLAlchemyObjectType, SQLAlchemyObjectType):
    class Meta:
        model = RecipeItem
        interfaces = (relay.Node,)

