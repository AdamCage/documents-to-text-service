from fastapi import Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from utils import (
    ImageConversionError,
    ImagePreprocessorError,
    TextExtractionError,
    S3UploadingError,
    BytesConvertingError,
    DataBaseWritingError,
    get_logger
)


logger = get_logger(__name__)


class ExceptionHandlers:

    @staticmethod
    def register(app):
        app.add_exception_handler(RequestValidationError, ExceptionHandlers.validation_exception_handler)
        app.add_exception_handler(ImageConversionError, ExceptionHandlers.image_conversion_exception_handler)
        app.add_exception_handler(ImagePreprocessorError, ExceptionHandlers.image_preprocessing_exception_handler)
        app.add_exception_handler(TextExtractionError, ExceptionHandlers.text_extraction_exception_handler)
        app.add_exception_handler(S3UploadingError, ExceptionHandlers.s3_uploading_exception_handler)
        app.add_exception_handler(BytesConvertingError, ExceptionHandlers.bytes_converting_exception_handler)
        app.add_exception_handler(DataBaseWritingError, ExceptionHandlers.database_writing_exception_handler)


    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Request validation error: {request.url}, errors: {exc.errors()}")
        return await request_validation_exception_handler(request, exc)


    @staticmethod
    async def image_conversion_exception_handler(exc: ImageConversionError):
        return JSONResponse(status_code=400, content={"detail": exc.message})


    @staticmethod
    async def image_preprocessing_exception_handler(exc: ImagePreprocessorError):
        return JSONResponse(status_code=500, content={"detail": exc.message})


    @staticmethod
    async def text_extraction_exception_handler(exc: TextExtractionError):
        return JSONResponse(status_code=500, content={"detail": exc.message})
    

    @staticmethod
    async def s3_uploading_exception_handler(exc: S3UploadingError):
        return JSONResponse(status_code=500, content={"detail": exc.message})


    @staticmethod
    async def bytes_converting_exception_handler(exc: BytesConvertingError):
        return JSONResponse(status_code=500, content={"detail": exc.message})


    @staticmethod
    async def database_writing_exception_handler(exc: DataBaseWritingError):
        return JSONResponse(status_code=500, content={"detail": exc.message})
