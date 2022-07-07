
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy import create_engine


from settings import Settings

engine = create_engine(Settings().DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async_engine = create_async_engine(Settings().DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)


def get_session():
    """
    This is just an async method to get the session

    :return:
    """

    session: Session = SessionLocal()

    try:
        yield session
    except Exception as e:
        session.rollback()

        raise e

    finally:
        session.close()


async def get_async_session():
    """

    :return:
    """

    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                yield session
            except Exception as e:
                await session.rollback()

                raise e
