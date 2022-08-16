import fastapi

from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette_exporter.optional_metrics import response_body_size, \
    request_body_size


def create_app():
    from models.db.session import db

    from routes.tag import router as tag_router
    from routes.recipe import router as recipe_router

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
    async def startup():
        await db.init()
        await db.create_all()

    @app.on_event('shutdown')
    async def shutdown_event():
        await db.close()

    app.include_router(recipe_router)
    app.include_router(tag_router)

    return app


if __name__ == "__main__":

    create_app()
