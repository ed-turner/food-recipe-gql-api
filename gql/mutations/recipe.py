import graphene
from graphene.relay.node import from_global_id, to_global_id

from models.db.recipe import Recipe
from models.db.recipe_items import RecipeItem
from models.db.tags import Tags
from gql.fields.inputs import RecipeInputType


class CreateRecipe(graphene.Mutation):
    class Arguments:
        recipe = RecipeInputType(required=True)

    Output = graphene.types.String

    @staticmethod
    def mutate(parent, info, recipe):
        """

        :param parent:
        :param info:
        :param recipe:
        :return:
        """
        db_session = info.context["session"]

        db_recipe = Recipe()

        db_recipe.name = recipe.name
        db_recipe.description = recipe.description
        db_recipe.direction = recipe.direction

        if len(recipe.recipeTags) == 0:
            pass
        else:
            tags = []

            for tag in recipe.recipeTags:
                _tag = db_session.query(Tags).filter(Tags.name == tag.name).first()

                if _tag is None:
                    _tag = Tags(name=tag.name)
                    db_session.add(_tag)

                tags.append(
                    _tag
                )

            db_recipe.recipe_tags = tags

        if len(recipe.recipeItems) == 0:
            pass
        else:
            recipe_items = []

            for recipe_item in recipe.recipeItems:

                db_recipe_item = RecipeItem()

                db_recipe_item.name = recipe_item.name
                db_recipe_item.measureQuantity = recipe_item.measureQuantity
                db_recipe_item.measureUnit = recipe_item.measureUnit.lower()

                db_session.add(db_recipe_item)

                recipe_items.append(
                    db_recipe_item
                )

            db_recipe.recipe_items = recipe_items

        db_session.add(db_recipe)

        db_session.flush()

        recipe_id = db_recipe.id

        db_session.commit()

        return to_global_id("Recipe", recipe_id)


class ModifyRecipeName(graphene.Mutation):
    """

    """
    class Arguments:
        recipeId = graphene.Field(graphene.String, required=True)
        recipeName = graphene.Field(graphene.String, required=True)

    Output = graphene.Field(graphene.types.Boolean)

    @staticmethod
    def mutate(parent, info, recipeId, recipeName):
        """

        :param parent:
        :param info:
        :param recipeId:
        :param recipeName:
        :return:
        """
        db_session = info.context["session"]

        recipe = db_session.get(Recipe, from_global_id(recipeId)[1])

        recipe.name = recipeName

        db_session.commit()
