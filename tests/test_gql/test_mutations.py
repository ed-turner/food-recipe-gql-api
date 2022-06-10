from gql.schema import schema

from graphene.relay.node import from_global_id, to_global_id


def test_create_recipe_item(db_session, db_data):
    _data = dict(
        recipeItemId=to_global_id("RecipeItemObjectType", 1),
        recipeItemName="mango curry",
    )

    executed = schema.execute(
        """
        mutation ($recipeItemId: String!, $recipeItemName: String!) {
            modifyRecipeItemName(
            recipeItemId: $recipeItemId,
            recipeItemName: $recipeItemName
            )
        }
        """,
        variable_values=_data,
        context_value={"session": db_session},
    )
    assert executed.errors is None
    res = executed.data["modifyRecipeItemName"]

    assert res


def test_create_recipe(db_session, db_data):

    _data = {
        "name": "rice",
    }

    executed = schema.execute(
        """
        mutation ($data: RecipeInputType!) {
            createRecipe(
            recipe: $data
            )
        }
        """,
        variable_values={"data": _data},
        context_value={"session": db_session},
    )

    assert executed.errors is None
    recipe_id = executed.data["createRecipe"]

    invoice_id = from_global_id(recipe_id)[1]

    assert int(invoice_id) > 1

