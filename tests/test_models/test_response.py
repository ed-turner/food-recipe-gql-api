from pydantic import ValidationError

from models.response import PydanticRecipeWithItems, PydanticTags, PydanticRecipeItem


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


def test_pydantic_recipe_no_tags_no_items():

    try:
        res = PydanticRecipeWithItems(
            id=1,
            name="curry",
            direction="",
            description="",
        )

        assert len(res.recipeItems) == 0
        assert len(res.recipeTags) == 0

    except ValidationError:
        raise AssertionError


def test_pydantic_recipe_no_tags():

    try:
        res = PydanticRecipeWithItems(
            id=1,
            name="curry",
            direction="",
            description="",
            recipeTags=[
                PydanticTags(id=1, name="a")
            ]
        )

        assert len(res.recipeItems) == 0

    except ValidationError:
        raise AssertionError


def test_pydantic_recipe_no_items():

    try:
        res = PydanticRecipeWithItems(
            id=1,
            name="curry",
            direction="",
            description="",
            recipeItems=[
                PydanticRecipeItem(
                    id=1,
                    name="curry",
                    measureUnit="OZ",
                    measureQuantity=1.,
                    recipe_id=1
                )
            ]
        )

        assert len(res.recipeTags) == 0

    except ValidationError:
        raise AssertionError


def test_pydantic_recipe():

    try:
        res = PydanticRecipeWithItems(
            id=1,
            name="curry",
            direction="",
            description="",
            recipeTags=[
                PydanticRecipeItem(
                    id=1,
                    name="curry",
                    measureUnit="OZ",
                    measureQuantity=1.,
                    recipe_id=1
                )
            ],
            recipeItems=[
                PydanticRecipeItem(
                    id=1,
                    name="curry",
                    measureUnit="OZ",
                    measureQuantity=1.,
                    recipe_id=1
                )
            ]
        )

    except ValidationError:
        raise AssertionError
