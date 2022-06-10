from models.db.recipe_items import RecipeItem


def test_get_recipe_item(db_session, db_data):
    recipe_item: RecipeItem = db_session.get(RecipeItem, 1)

    assert not recipe_item is None
