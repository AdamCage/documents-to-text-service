from fastapi import FastAPI

from core import config
from setupers import setup_prometheus, setup_middlewares, setup_routes, setup_cors
from exception_handlers import ExceptionHandlers
from lifespan import lifespan


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=config.service_info["name"],
        version=config.service_info["version"],
        lifespan=lifespan
    )

    setup_prometheus(app)
    setup_middlewares(app)
    setup_routes(app)
    setup_cors(app)

    ExceptionHandlers.register(app)

    return app
