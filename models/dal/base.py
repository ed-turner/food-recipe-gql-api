from typing import Generic, TypeVar, List
from sqlalchemy.sql.expression import delete, update, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from ..db.base import Base

T = TypeVar('T', bound=Base)


class AsyncDAL(Generic[T]):
    """

    """
    def __init__(self, session: AsyncSession):
        """

        :param session:
        """
        self.session: AsyncSession = session

    async def get(self, db_id) -> T:
        """

        :param db_id:
        :return:
        """
        return await self.session.get(T, db_id)

    async def delete(self, db_id: int):
        """

        :param db_id:
        :return:
        """
        stmt = delete(T).filter_by(id=db_id)

        await self.session.execute(stmt)

    async def update(self, db_id: int, **kwargs):
        """

        :param db_id:
        :param kwargs:
        :return:
        """

        if kwargs:
            stmt = update(T).filter_by(id=db_id)

            stmt = stmt.values(**kwargs)

            await self.session.execute(stmt)

    async def get_all(self, filter_kwargs: dict) -> List[T]:
        """

        :param filter_kwargs:
        :return:
        """
        stmt = select(T)

        return await self.session.execute(stmt)
