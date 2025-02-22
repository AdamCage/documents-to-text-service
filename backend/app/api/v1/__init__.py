from fastapi import APIRouter

from .health import router as health_router
from .reset_metrics import router as metrics_router
from .extract_text_from_image import router as image_router
from .extract_text_from_pdf import router as pdf_router


v1_routers = APIRouter()


v1_routers.include_router(health_router, prefix="/health", tags=["health"])
v1_routers.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
v1_routers.include_router(image_router, prefix="/extract_text_from_image", tags=["image"])
v1_routers.include_router(pdf_router, prefix="/extract_text_from_pdf", tags=["pdf"])
