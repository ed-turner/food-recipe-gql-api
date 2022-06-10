import graphene

from .mutations.recipe import CreateRecipe
from .mutations.recipe_item import ModifyRecipeItemName, ModifyRecipeItemMeasureUnit, \
    ModifyRecipeItemMeasureQuantity


class Mutation(graphene.ObjectType):

    createRecipe = CreateRecipe.Field()

    modifyRecipeItemName = ModifyRecipeItemName.Field()

    modifyRecipeItemMeasureUnit = ModifyRecipeItemMeasureUnit.Field()

    modifyRecipeItemMeasureQuantity = ModifyRecipeItemMeasureQuantity.Field()
