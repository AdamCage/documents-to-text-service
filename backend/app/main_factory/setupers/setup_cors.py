import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import config
from utils import CORSOrigins


def setup_cors(app: FastAPI, logger: logging.Logger):
    """Configure CORS settings for the application."""
    cors_origins = CORSOrigins(config, logger)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins.origins,
        allow_credentials=True,
        allow_methods=cors_origins.methods,
        allow_headers=cors_origins.headers
    )
