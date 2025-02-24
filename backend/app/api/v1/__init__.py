from fastapi import APIRouter

from .health import router as health_router
from .reset_metrics import router as metrics_router
from .extract_text_from_image import router as image_router
from .extract_text_from_pdf import router as pdf_router
from .extract_text_from_image_with_llm_correction import router as image_llm_router
from .extract_text_from_pdf_with_llm_corrections import router as pdf_llm_router


v1_routers = APIRouter()


v1_routers.include_router(health_router, prefix="/v1", tags=["health"])
v1_routers.include_router(metrics_router, prefix="/v1", tags=["metrics"])
v1_routers.include_router(image_router, prefix="/v1", tags=["image"])
v1_routers.include_router(pdf_router, prefix="/v1", tags=["pdf"])
v1_routers.include_router(image_llm_router, prefix="/v1", tags=["image", "llm"])
v1_routers.include_router(pdf_llm_router, prefix="/v1", tags=["pdf", "llm"])
