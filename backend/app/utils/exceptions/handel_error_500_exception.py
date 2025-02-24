import logging
from functools import wraps
from typing import Callable

from fastapi import HTTPException


def handel_error_500_exception(logger: logging.Logger):


    def decorator(func: Callable):


        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            
            except Exception as e:
                msg = str(e)
                logger.error(msg)
                raise HTTPException(status_code=500, detail=msg)
            
        return wrapper
    

    return decorator