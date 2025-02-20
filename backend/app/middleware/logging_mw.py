from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable

from utils.logger import get_logger


logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """_summary_

    Args:
        BaseHTTPMiddleware (_type_): _description_
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """_summary_

        Args:
            request (Request): _description_
            call_next (Callable[[Request], Awaitable[Response]]): _description_

        Returns:
            Response: _description_
        """
        logger.info(f'Received request: Method - {request.method} URL - {request.url} Headers - {request.headers} BodyJSON - {request.json()}')
        response: Response = await call_next(request)
        
        return response
