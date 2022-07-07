

class SessionSQLAlchemyObjectType:
    """
    This is a mix to get an async db session
    """

    @classmethod
    def get_node(cls, info, id):
        session = info.context["session"]

        return session.get(cls._meta.model, int(id))


class AsyncSessionSQLAlchemyObjectType:
    """
    This is a mix to get an async db session
    """

    @classmethod
    async def get_node(cls, info, id):
        session = info.context["session"]

        return await session.get(cls._meta.model, int(id))
