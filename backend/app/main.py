import asyncio
from contextlib import asynccontextmanager
from typing import Coroutine, Any, NoReturn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from middleware import LoggingMiddleware, metrics_middleware
from api.v1.endpoints import router as api_router
from core import config, http_format
from orm import db_engine
from system_metrics import update_hardware_metrics
from utils import get_logger, ImageConversionError, ImagePreprocessorError, \
    TextExtractionError, S3UploadingError, BytesConvertingError, DataBaseWritingError, \
        CORSOrigins


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> NoReturn:
    """_summary_

    Args:
        app (FastAPI): _description_

    Returns:
        NoReturn: _description_
    """
    # Startup event
    asyncio.create_task(update_hardware_metrics())
    logger.info(f'Starting {config.service_info["name"]} - {config.service_info["version"]}')

    db_engine.init_db()

    logger.info('Service started successfully.\n')
    
    yield

    # Shutdown event
    logger.info("Service turned off.\n")


app = FastAPI(
    title=config.service_info["name"],
    version=config.service_info["version"],
    lifespan=lifespan
)

prometheus_instrumentator = Instrumentator()
prometheus_instrumentator.instrument(app).expose(app, endpoint="/metrics")

app.add_middleware(LoggingMiddleware)
app.middleware(http_format)(metrics_middleware)
    
app.include_router(api_router, prefix=f"/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Coroutine[Any, Any, JSONResponse]:
    logger.error(f"Request validation error: {request.url}, errors: {exc.errors()}")

    return await request_validation_exception_handler(request, exc)


@app.exception_handler(ImageConversionError)
async def image_conversion_exception_handler(exc: ImageConversionError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


@app.exception_handler(ImagePreprocessorError)
async def image_preprocessing_exception_handler(exc: ImagePreprocessorError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


@app.exception_handler(TextExtractionError)
async def image_text_extraction_exception_handler(exc: TextExtractionError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


@app.exception_handler(S3UploadingError)
async def image_text_extraction_exception_handler(exc: S3UploadingError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


@app.exception_handler(BytesConvertingError)
async def image_text_extraction_exception_handler(exc: BytesConvertingError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


@app.exception_handler(DataBaseWritingError)
async def image_text_extraction_exception_handler(exc: DataBaseWritingError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


cors_origins = CORSOrigins(config, logger)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins.origins,
    allow_credentials=True,
    allow_methods=cors_origins.methods,
    allow_headers=cors_origins.headers
)
