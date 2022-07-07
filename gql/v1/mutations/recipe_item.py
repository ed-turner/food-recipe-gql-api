import graphene
from graphene.relay.node import from_global_id

from models.db.recipe_items import RecipeItem
from ..fields.inputs import RecipeItemInputType


class CreateRecipeItem(graphene.Mutation):

    class Arguments:
        recipeItem = RecipeItemInputType(required=True)
        recipeId = graphene.Argument(graphene.String, required=True)

    Output = graphene.types.Boolean

    @staticmethod
    def mutate(parent, info, recipeId, recipeItem):
        """

        :param parent:
        :param info:
        :param recipeId:
        :param recipeItem:
        :return:
        """
        db_session = info.context["session"]

        db_recipe_item = RecipeItem()

        db_recipe_item.name = recipeItem.name
        db_recipe_item.measureQuantity = recipeItem.measureQuantity
        db_recipe_item.measureUnit = recipeItem.measureUnit
        db_recipe_item.recipe_id = int(from_global_id(recipeId)[1])

        db_session.add(db_recipe_item)

        db_session.commit()

        return True


class ModifyRecipeItemName(graphene.Mutation):
    class Arguments:
        recipeItemId = graphene.Argument(graphene.String, required=True)
        recipeItemName = graphene.Argument(graphene.String, required=True)

    Output = graphene.types.Boolean

    @staticmethod
    def mutate(parent, info, recipeItemId, recipeItemName):
        """

        :param parent:
        :param info:
        :param recipeItemId:
        :param recipeItemName:
        :return:
        """
        db_session = info.context["session"]

        db_recipe_item = db_session.get(RecipeItem, from_global_id(recipeItemId)[1])

        db_recipe_item.name = recipeItemName

        db_session.commit()

        return True


class ModifyRecipeItemMeasureUnit(graphene.Mutation):
    class Arguments:
        recipeItemId = graphene.Argument(graphene.String, required=True)
        recipeItemUnit = graphene.Argument(graphene.Float, required=True)

    Output = graphene.types.Boolean

    @staticmethod
    def mutate(parent, info, recipeItemId, recipeItemUnit):
        """

        :param parent:
        :param info:
        :param recipeItemId:
        :param recipeItemUnit:
        :return:
        """
        db_session = info.context["session"]

        db_recipe_item: RecipeItem = db_session.get(RecipeItem, from_global_id(recipeItemId)[1])

        db_recipe_item.measureUnit = recipeItemUnit

        db_session.commit()

        return True


class ModifyRecipeItemMeasureQuantity(graphene.Mutation):
    class Arguments:
        recipeItemId = graphene.Argument(graphene.String, required=True)
        recipeItemQuantity = graphene.Argument(graphene.String, required=True)

    Output = graphene.types.Boolean

    @staticmethod
    def mutate(parent, info, recipeItemId, recipeItemQuantity):
        """

        :param parent:
        :param info:
        :param recipeItemId:
        :param recipeItemQuantity:
        :return:
        """
        db_session = info.context["session"]

        db_recipe_item: RecipeItem = db_session.get(RecipeItem, from_global_id(recipeItemId)[1])

        db_recipe_item.measureQuantity = recipeItemQuantity

        db_session.commit()

        return True
