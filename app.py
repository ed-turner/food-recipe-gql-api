import fastapi
from gql.schema import schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette_exporter.optional_metrics import response_body_size, \
    request_body_size


def create_app():
    from models.db.session import get_session, engine
    from models.db.base import Base

    app = fastapi.FastAPI()

    @app.get("/health")
    def health_check():
        return "ping"

    app.mount("/", GraphQLApp(
        schema,
        on_get=make_graphiql_handler(),
        context_value={"session": lambda: get_session()}
    )
              )  # Graphiql IDE

    app.add_middleware(
        PrometheusMiddleware,
        group_paths=True,
        app_name="foodRecipeAPI",
        optional_metrics=[response_body_size, request_body_size]
    )
    app.add_route("/metrics", handle_metrics)

    @app.on_event("startup")
    def startup():
        try:
            Base.metadata.create_all(engine)
        except:
            pass



# @app.post("/graphql")
# async def post_graphql(
#     request: fastapi.Request,
#     session: Session = Depends(get_session),
# ):
#     content_type = request.headers.get("Content-Type", "")
#
#     if "application/json" in content_type:
#         data = await request.json()
#
#     elif "application/graphql" in content_type:
#         body = await request.body()
#         text = body.decode()
#         data = {"query": text}
#
#     elif "query" in request.query_params:
#         data = request.query_params
#
#     else:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             detail="Unsupported Media Type",
#         )
#
#     if not (q_body := data.get("query")):
#         raise fastapi.HTTPException(status_code=400, detail=f"Unsupported method: {q_body}")
#
#     res = await schema.execute_async(
#         q_body,
#         context_value={"request": request, "session": session},
#     )
#
#     return res.to_dict()

if __name__ == "__main__":

    create_app()