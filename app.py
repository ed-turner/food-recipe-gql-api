import fastapi

from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette_exporter.optional_metrics import response_body_size, \
    request_body_size

from gql.v1.schema import schema


def create_app():
    from models.db.session import get_session, engine
    from models.db.base import Base

    app = fastapi.FastAPI()

    @app.get("/health")
    def health_check():
        return "ping"

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

    @app.post("/")
    async def post_graphql(
            request: fastapi.Request,
            session=fastapi.Depends(get_session),
    ):
        content_type = request.headers.get("Content-Type", "")

        if "application/json" in content_type:
            data = await request.json()

        elif "application/graphql" in content_type:
            body = await request.body()
            text = body.decode()
            data = {"query": text}

        elif "query" in request.query_params:
            data = request.query_params

        else:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported Media Type",
            )

        if not (q_body := data.get("query")):
            raise fastapi.HTTPException(status_code=400, detail=f"Unsupported method: {q_body}")

        res = schema.execute(
            q_body,
            context_value={"request": request, "session": session},
        )

        res_dict = {"data": res.data}

        if res.errors is None:
            pass
        else:
            res_dict["errors"] = str(res.errors)

        return res_dict

    return app


if __name__ == "__main__":

    create_app()
