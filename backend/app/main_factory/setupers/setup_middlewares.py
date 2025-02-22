from fastapi import FastAPI

from middleware import LoggingMiddleware, metrics_middleware


def setup_middlewares(app: FastAPI):
    """Add middlewares to the application."""
    app.add_middleware(LoggingMiddleware)
    app.middleware(metrics_middleware)
