import graphene
from graphene import relay
from graphene_sqlalchemy_filter import FilterableConnectionField

from gql.fields.objects import RecipeObjectType, TagObjectType, RecipeItemObjectType
from gql.fields.filters import RecipeFilter, RecipeItemFilter, TagsFilter


class Query(graphene.ObjectType):
    """

    """
    node = relay.Node.Field()

    recipes = FilterableConnectionField(
        RecipeObjectType.connection,
        filters=RecipeFilter()
    )

    recipe_items = FilterableConnectionField(
        RecipeItemObjectType.connection,
        filters=RecipeItemFilter()
    )

    tags = FilterableConnectionField(
        TagObjectType.connection,
        filters=TagsFilter()
    )
