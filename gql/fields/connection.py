

class AsyncConnectionField:
    """

    """

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
            resolved = cls.get_query(model, info, **args)
        if isinstance(resolved, Query):
            _len = resolved.count()
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