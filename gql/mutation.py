import graphene

from .mutations.recipe import ModifyRecipeName, RemoveRecipe, \
    RemoveRecipeTag, CreateRecipe
from .mutations.recipe_item import ModifyRecipeItemName, ModifyRecipeItemMeasureUnit, \
    ModifyRecipeItemMeasureQuantity


class Mutation(graphene.ObjectType):

    createRecipe = CreateRecipe.Field()

    modifyRecipeName = ModifyRecipeName.Field()

    removeRecipe = RemoveRecipe.Field()

    removeRecipeTag = RemoveRecipeTag.Field()

    modifyRecipeItemName = ModifyRecipeItemName.Field()

    modifyRecipeItemMeasureUnit = ModifyRecipeItemMeasureUnit.Field()

    modifyRecipeItemMeasureQuantity = ModifyRecipeItemMeasureQuantity.Field()
