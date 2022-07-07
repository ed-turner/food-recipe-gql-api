from graphene.relay.node import to_global_id, from_global_id
from gql.v1.schema import schema


def test_get_recipe(db_session, db_data):
    global_id = to_global_id("RecipeObjectType", 1)
    executed = schema.execute(
        """
        query Node($id: ID!) {
            node(id: $id) {
                ... on RecipeObjectType {
                    id
                }
            }
        }
        """,
        variable_values={"id": global_id},
        context_value={"session": db_session},
    )
    assert executed.errors is None
    user = executed.data["node"]
    invoice_id = from_global_id(user["id"])[1]

    assert invoice_id == str(1)


def test_get_recipe_item(db_session, db_data):
    global_id = to_global_id("RecipeItemObjectType", 1)
    executed = schema.execute(
        """
        query Node($id: ID!) {
            node(id: $id) {
                ... on RecipeItemObjectType {
                    id
                    name
                }
            }
        }
        """,
        variable_values={"id": global_id},
        context_value={"session": db_session},
    )
    assert executed.errors is None
    user = executed.data["node"]
    invoice_id = from_global_id(user["id"])[1]

    assert user["name"] == "curry"
    assert invoice_id == str(1)


def test_get_tag(db_session, db_data):
    global_id = to_global_id("TagObjectType", 1)
    executed = schema.execute(
        """
        query Node($id: ID!) {
            node(id: $id) {
                ... on TagObjectType {
                    id
                    name
                }
            }
        }
        """,
        variable_values={"id": global_id},
        context_value={"session": db_session},
    )
    assert executed.errors is None
    user = executed.data["node"]
    invoice_id = from_global_id(user["id"])[1]

    assert user["name"] == "indian"
    assert invoice_id == str(1)


def test_get_tagged_recipes(db_session, db_data):
    global_id = to_global_id("TagObjectType", 1)
    executed = schema.execute(
        """
        query Node($id: ID!) {
            node(id: $id) {
                ... on TagObjectType {
                    id
                    name
                    taggedRecipes {
                        edges {
                            node {
                                name
                            }
                        }
                    }
                }
            }
        }
        """,
        variable_values={"id": global_id},
        context_value={"session": db_session},
    )
    assert executed.errors is None
    user = executed.data["node"]
    invoice_id = from_global_id(user["id"])[1]

    assert user["name"] == "indian"
    assert invoice_id == str(1)

    assert len(user["taggedRecipes"]["edges"]) == 2


def test_get_recipes(db_session, db_data):

    executed = schema.execute(
        """
        query Recipes {
            recipes
            {
                edges {
                    node {
                        id
                    }
                }
            }
        }
        """,
        context_value={"session": db_session},
    )
    assert executed.errors is None
    recipes = executed.data["recipes"]["edges"]

    assert len(recipes) == 2
