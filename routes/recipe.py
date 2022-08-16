from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.sql.operators import ilike_op
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException

from models.db.session import get_async_session, AsyncSession

from models.db.recipe import Recipe
from models.db.recipe_items import RecipeItem
from models.db.tags import Tags
from models.response import PydanticRecipe, PydanticRecipeItem, \
    PydanticRecipeWithItemsWithTags

router = APIRouter(prefix="/recipe")

#  GET METHODS


@router.get("/get/{recipe_id}")
async def get_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PydanticRecipeWithItemsWithTags:
    """

    :param recipe_id:
    :param session:
    :return:
    """
    stmt = select(Recipe).where(Recipe.id == recipe_id).options(
        selectinload(Recipe.recipe_items)
    ).options(
        selectinload(Recipe.recipe_tags)
    )

    return (await session.execute(stmt)).scalar()


@router.get("/page")
async def get_page(
    skip: int = 0, limit: int = 10,
    session: AsyncSession = Depends(get_async_session)
) -> List[PydanticRecipe]:
    """

    :param skip:
    :param limit:
    :param session:
    :return:
    """

    stmt = select(Recipe).offset(skip*limit).limit(limit)

    res = await session.execute(stmt)

    return res.all()


@router.get("/search")
async def find_recipe(
        recipe_name: Optional[str] = None,
        recipe_item_name: Optional[str] = None,
        recipe_tag: Optional[str] = None,
        session: AsyncSession = Depends(get_async_session)
) -> List[PydanticRecipe]:
    """

    :param recipe_name:
    :param recipe_item_name:
    :param recipe_tag:
    :param session:
    :return:
    """
    if all(
            [recipe_tag is None,
             recipe_name is None,
             recipe_item_name is None]
    ):
        raise HTTPException(
            status_code=404,
            detail="All search parameters are none"
        )

    stmt = select(Recipe)

    if recipe_name:
        stmt = stmt.where(ilike_op(Recipe.name, f"%{recipe_name}%"))

    if recipe_tag:
        stmt = stmt.join(Tags.tagged_recipes).where(Tags.name == recipe_tag)

    if recipe_item_name:
        stmt = stmt.join(RecipeItem.recipe).where(
            ilike_op(RecipeItem.name, f"%{recipe_item_name}%")
        )

    return (await session.execute(stmt)).all()


@router.post("/create")
async def create_recipe(
    recipe: PydanticRecipe,
    session: AsyncSession = Depends(get_async_session)
) -> int:
    """

    :param recipe:
    :param session:
    :return:
    """

    # searches if we already have a recipe with the exact name
    stmt = select(Recipe).where(Recipe.name == recipe.name)

    res = await session.execute(stmt)

    if res.scalar():
        raise HTTPException(status_code=404, detail="The recipe already exists")

    db_recipe = Recipe()

    db_recipe.name = recipe.name
    db_recipe.description = recipe.description
    db_recipe.direction = recipe.direction

    session.add(db_recipe)

    await session.flush()

    recipe_id = db_recipe.id

    await session.commit()

    return recipe_id


@router.post("/{recipe_id}/tag")
async def tag_recipe(
    recipe_id: int,
    tag: str,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    """

    :param recipe_id:
    :param tag:
    :param session:
    :return:
    """

    stmt = select(Tags).filter(Tags.name == tag).filter(
        Tags.tagged_recipes.has(
            Recipe.id == recipe_id
        )
    )

    res = await session.execute(stmt)

    if res.scalar():
        raise HTTPException(status_code=404, detail="The recipe already exists")

    stmt = select(Tags).filter(Tags.name == tag)

    res = await session.execute(stmt)

    db_tag = res.scalar()
    db_recipe = await session.get(Recipe, recipe_id)

    if db_tag:
        db_tag.tagged_recipes.append(
            db_recipe
        )
    else:
        db_tag = Tags()
        db_tag.name = tag

        db_tag.tagged_recipes = [db_recipe]

        session.add(db_tag)

    await session.commit()


@router.post("/{recipe_id}/item/add")
async def add_item_to_recipe(
        recipe_id: int,
        recipe_item: PydanticRecipeItem,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    """

    :param recipe_id:
    :param recipe_item:
    :param session:
    :return:
    """