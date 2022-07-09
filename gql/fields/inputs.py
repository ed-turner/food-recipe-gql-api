import graphene

from graphene.types import InputObjectType


class TagInputType(InputObjectType):
    """

    """
    name = graphene.String(required=True)


class RecipeItemInputType(InputObjectType):
    """

    """

    name = graphene.String(required=True)
    measureQuantity = graphene.Float(required=True)
    measureUnit = graphene.String(required=True)


class RecipeInputType(InputObjectType):
    """

    """

    name = graphene.String(required=True)
    description = graphene.String()
