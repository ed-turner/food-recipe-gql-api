from pydantic import ValidationError

from models.response import PydanticRecipe, PydanticTags, PydanticRecipeItem


def test_pydantic_tag():

    try:
        _ = PydanticTags(id=1, name="a")
    except ValidationError:
        raise AssertionError


def test_pydantic_recipe_item():

    try:
        _ = PydanticRecipeItem(
            id=1,
            name="curry",
            measureUnit="OZ",
            measureQuantity=1.,
            recipe_id=1
        )
    except ValidationError:
        raise AssertionError


def test_pydantic_recipe():

    try:
        _ = PydanticRecipe(
            id=1,
            name="curry",
            direction="",
            description="",
        )

    except ValidationError:
        raise AssertionError

