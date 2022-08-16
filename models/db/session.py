
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from .base import Base

from settings import Settings


class Database:
    def __init__(self, url):
        self._session = None
        self._engine = None

        if "asyncpg" in url:
            pass
        else:
            url = url.replace("postgresql", "postgresql+asyncpg")

        self.url = url

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def __getattr__(self, name) -> AsyncSession:
        return getattr(self._session, name)

    async def init(self):
        # closes connections if a session is created,
        # so as not to create repeated connections
        if self._session:
            await self._session.close()

        self._engine = create_async_engine(self.url, future=True)
        self._session = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )()


DATABASE_URL = Settings().DATABASE_URL

db: Database = Database(DATABASE_URL)


async def get_async_session():
    """

    :return:
    """

    # async with db._session() as session:
    async with db.begin():
        try:
            yield db
        except Exception as e:
            await db.rollback()

            raise e
        finally:
            await db.close()
