from graphene_pydantic import PydanticInputObjectType

from models.response import PydanticTags, PydanticRecipeItem, PydanticRecipe


class TagInputType(PydanticInputObjectType):
    """

    """

    class Meta:
        model = PydanticTags
        exclude_fields = ("id",)
        # exclude specified fields


class RecipeItemInputType(PydanticInputObjectType):
    """

    """

    class Meta:
        model = PydanticRecipeItem
        exclude_fields = ("id", "recipeId")
        # exclude specified fields


class RecipeInputType(PydanticInputObjectType):
    """

    """

    class Meta:
        model = PydanticRecipe
        exclude_fields = ("id",)
        # exclude specified fields


TagInputType.resolve_placeholders()
RecipeItemInputType.resolve_placeholders()
RecipeInputType.resolve_placeholders()
