import graphene

from graphene.types import InputObjectType
from models.response import PydanticTags, PydanticRecipeItem


class TagInputType(InputObjectType):
    """

    """
    name = graphene.String(required=True)


class RecipeItemInputType(InputObjectType):
    """

    """

    class Meta:
        model = PydanticRecipeItem
        exclude_fields = ("id", "recipeId")
        # exclude specified fields


class RecipeInputType(InputObjectType):
    """

    """

    name = graphene.String(required=True)
    description = graphene.String()
