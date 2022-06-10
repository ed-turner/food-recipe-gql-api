from models.db.recipe import Recipe


def test_get_recipe(db_session, db_data):
    recipe: Recipe = db_session.get(Recipe, 1)

    assert not recipe is None
    assert recipe.name == "curry"


def test_get_recipe_1_items(db_session, db_data):
    recipe: Recipe = db_session.get(Recipe, 1)

    assert not recipe is None
    assert len(recipe.recipe_items) == 1


def test_get_recipe_1_tags(db_session, db_data):
    recipe: Recipe = db_session.get(Recipe, 1)

    assert not recipe is None
    assert len(recipe.recipe_tags) == 1


