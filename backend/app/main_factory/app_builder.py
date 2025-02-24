from fastapi import FastAPI

from core import config
from utils import get_logger
from .setupers import setup_prometheus, setup_middlewares, setup_routes, setup_cors, setup_logger
from .exception_handlers import ExceptionHandlers
from .lifespan import lifespan


logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=config.service_info["name"],
        version=config.service_info["version"],
        lifespan=lifespan
    )

    setup_logger(config)

    setup_prometheus(app)
    setup_middlewares(app)
    setup_routes(app)
    setup_cors(app, logger)

    ExceptionHandlers.register(app)

    return app
