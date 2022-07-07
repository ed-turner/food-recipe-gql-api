import enum
from functools import partial

from promise import Promise, is_thenable

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy.sql.expression import select
from graphene.relay.connection import connection_adapter, page_info_adapter
from graphene_sqlalchemy.utils import EnumValue
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphql_relay.connection.arrayconnection import \
    connection_from_array_slice


def _get_async_session(context) -> AsyncSession:
    return context.get("session")


def _get_session(context):
    return context.get("session")()


def _get_query(model, context):
    query = getattr(model, "query", None)
    if not query:
        session = _get_session(context)
        if not session:
            raise Exception(
                "A query in the model Base or a session in the schema is required for querying.\n"
                "Read more http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tips/#querying"
            )
        query = session.query(model)
    return query


def _get_async_query(model, context):
    query = getattr(model, "query", None)
    if not query:
        session = _get_async_session(context)
        if not session:
            raise Exception(
                "A query in the model Base or a session in the schema is required for querying.\n"
                "Read more http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tips/#querying"
            )

        query = session.query(model)
    return query


class SessionConnectionField(SQLAlchemyConnectionField):
    """

    """

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = _get_query(model, info.context)
        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
            sort_args = []
            # ensure consistent handling of graphene Enums, enum values and
            # plain strings
            for item in sort:
                if isinstance(item, enum.Enum):
                    sort_args.append(item.value.value)
                elif isinstance(item, EnumValue):
                    sort_args.append(item.value)
                else:
                    sort_args.append(item)
            query = query.order_by(*sort_args)
        return query


class AsyncSessionConnectionField(SQLAlchemyConnectionField):
    """

    """

    @classmethod
    async def get_query(self, model, info, sort=None, **args):
        """

        :return:
        """
        session = _get_async_session(info.context)

        stmt = select(model)

        if sort is not None:
            if not isinstance(sort, list):
                sort = [sort]
            sort_args = []
            # ensure consistent handling of graphene Enums, enum values and
            # plain strings
            for item in sort:
                if isinstance(item, enum.Enum):
                    sort_args.append(item.value.value)
                elif isinstance(item, EnumValue):
                    sort_args.append(item.value)
                else:
                    sort_args.append(item)

            stmt = stmt.order_by(*sort_args)

        results = await session.execute(stmt)

        return results.scalars().all()

    @classmethod
    async def resolve_connection(cls, connection_type, model, info, args, resolved):
        """

        :param connection_type:
        :param model:
        :param info:
        :param args:
        :param resolved:
        :return:
        """
        if resolved is None:
            resolved = await cls.get_query(model, info, **args)
        if isinstance(resolved, AsyncResult):
            resolved = await resolved.all()
            _len = len(resolved)
        else:
            _len = len(resolved)

        def adjusted_connection_adapter(edges, pageInfo):
            return connection_adapter(connection_type, edges, pageInfo)

        connection = connection_from_array_slice(
            array_slice=resolved,
            args=args,
            slice_start=0,
            array_length=_len,
            array_slice_length=_len,
            connection_type=adjusted_connection_adapter,
            edge_type=connection_type.Edge,
            page_info_type=page_info_adapter,
        )
        connection.iterable = resolved
        connection.length = _len
        return connection

    @classmethod
    async def connection_resolver(cls, resolver, connection_type, model, root, info, **args):
        """

        :param resolver:
        :param connection_type:
        :param model:
        :param root:
        :param info:
        :param args:
        :return:
        """
        resolved = resolver(root, info, **args)

        on_resolve = partial(cls.resolve_connection, connection_type, model, info, args)
        if is_thenable(resolved):
            return Promise.resolve(resolved).then(on_resolve)

        return on_resolve(resolved)
