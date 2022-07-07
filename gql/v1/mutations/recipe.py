import graphene
from graphene.relay.node import from_global_id, to_global_id
from sqlalchemy.sql.expression import delete

from models.db.recipe import Recipe
from models.db.associations import recipe_tags_table
from gql.v1.fields.inputs import RecipeInputType


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

        # if len(recipe.recipeTags) == 0:
        #     pass
        # else:
        #     tags = []
        #
        #     for tag in recipe.recipeTags:
        #         _tag = db_session.query(Tags).filter(Tags.name == tag.name).first()
        #
        #         if _tag is None:
        #             _tag = Tags(name=tag.name)
        #             db_session.add(_tag)
        #
        #         tags.append(
        #             _tag
        #         )
        #
        #     db_recipe.recipe_tags = tags

        db_session.add(db_recipe)

        db_session.flush()

        recipe_id = db_recipe.id

        db_session.commit()

        return to_global_id("Recipe", recipe_id)


class ModifyRecipeName(graphene.Mutation):
    """

    """
    class Arguments:
        recipeId = graphene.Argument(graphene.String, required=True)
        recipeName = graphene.Argument(graphene.String, required=True)

    Output = graphene.types.Boolean

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


class RemoveRecipe(graphene.Mutation):
    """

    """
    class Arguments:
        recipeId = graphene.Argument(graphene.String, required=True)

    Output = graphene.types.Boolean

    @staticmethod
    def mutate(parent, info, recipeId):
        """

        :param parent:
        :param info:
        :param recipeId:
        :return:
        """
        db_session = info.context["session"]

        recipe = db_session.get(Recipe, from_global_id(recipeId)[1])

        db_session.delete(recipe)

        db_session.commit()


class RemoveRecipeTag(graphene.Mutation):

    class Arguments:
        recipeId = graphene.Argument(graphene.String, required=True)
        tagId = graphene.Argument(graphene.String, required=True)

    Output = graphene.types.Boolean

    @staticmethod
    def mutate(parent, info, recipeId, tagId):
        """

        :param parent:
        :param info:
        :param recipeId:
        :param tagId:
        :return:
        """
        db_session = info.context["session"]

        statement = delete(recipe_tags_table).where(
            recipe_tags_table.recipe_id == int(from_global_id(recipeId)[1]),
            recipe_tags_table.tag_id == int(from_global_id(tagId)[1])
        )

        db_session.execute(statement)
