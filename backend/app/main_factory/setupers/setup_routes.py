from fastapi import FastAPI

from api import app_routers


def setup_routes(app: FastAPI) -> None:
    app.include_router(app_routers)
