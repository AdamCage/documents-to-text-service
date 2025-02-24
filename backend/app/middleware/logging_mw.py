from json import JSONDecodeError
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from utils.logger import get_logger


logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """_summary_

    Args:
        BaseHTTPMiddleware (_type_): _description_
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if request.method != "OPTIONS":
            if "multipart/form-data" in request.headers.get("content-type", ""):
                body = "<FILE CONTENT>"

            else:
                try:
                    body = await request.json()
                    
                except JSONDecodeError:
                    body = await request.body()
            
            logger.info(f'Received request: Method - {request.method} URL - {request.url} Headers - {request.headers} Body - {body}')
        
        response = await call_next(request)
        return response
