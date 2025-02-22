import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core import config
from orm import db_engine
from system_metrics import update_hardware_metrics
from utils import get_logger


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the FastAPI application."""
    # Startup event
    asyncio.create_task(update_hardware_metrics())
    logger.info(f'Starting {config.service_info["name"]} - {config.service_info["version"]}')
    
    db_engine.init_db()
    logger.info('Service started successfully.\n')
    
    yield

    # Shutdown event
    logger.info("Service turned off.\n")
