import pytest

import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient

from models.db.base import Base
from models.db.recipe import Recipe
from models.db.recipe_items import RecipeItem
from models.db.tags import Tags

from app import create_app


@pytest.fixture
def db_session(postgresql):

    connection = f'postgresql://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'

    engine = create_engine(connection)
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    try:
        yield session
    finally:
        session.close()

    Base.metadata.drop_all(engine)


@pytest.fixture
def db_data(db_session):
    """

    :param db_session:
    :return:
    """

    tag = Tags(name="indian")

    recipe_item = RecipeItem(
        name="curry",
        measureUnit="OZ",
        measureQuantity=1.
    )

    recipe = Recipe(
        name="curry",
        direction="",
        description=""
    )

    recipe2 = Recipe(
        name="vinladoo",
        direction="",
        description=""
    )

    recipe.recipe_items = [recipe_item]
    recipe.recipe_tags = [tag]

    recipe2.recipe_tags = [tag]

    db_session.add(recipe)
    db_session.flush()

    db_session.add(recipe2)

    db_session.commit()


@pytest.fixture
def api_client(postgresql, db_data):

    connection = f"postgresql://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"

    os.environ["DATABASE_URL"] = connection

    return TestClient(create_app())
