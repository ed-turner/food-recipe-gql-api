from fastapi import APIRouter, Depends, HTTPException

from models.db.session import get_async_session, AsyncSession

from models.db.tags import Tags

router = APIRouter(prefix="/tag")


@router.post("/create")
async def create_tag(
        name: str,
        session: AsyncSession = Depends(get_async_session)) -> None:
    """

    :param name:
    :param session:
    :return:
    """

    session.add(
        Tags(name=name)
    )

    await session.commit()
