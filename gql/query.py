import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from gql.fields.objects import RecipeObjectType, TagObjectType, RecipeItemObjectType


class Query(graphene.ObjectType):
    """

    """
    node = relay.Node.Field()

    recipes = SQLAlchemyConnectionField(
        RecipeObjectType.connection
    )

    recipe_items = SQLAlchemyConnectionField(
        RecipeItemObjectType.connection
    )

    tags = SQLAlchemyConnectionField(
        TagObjectType.connection
    )
