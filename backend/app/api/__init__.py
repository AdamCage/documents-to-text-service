from fastapi import APIRouter

from .v1 import v1_routers


app_routers = APIRouter()

app_routers.include_router(v1_routers, prefix="/api")


__all__ = [
    "app_routers"
]
