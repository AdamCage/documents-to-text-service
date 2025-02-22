from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils import get_logger, handel_error_500_exception


logger = get_logger(__name__)

router = APIRouter()


@router.get("/reset_metrics")
@handel_error_500_exception(logger)
async def reset_metrics() -> JSONResponse:
    reset_metrics()
    return JSONResponse(content={"message": "metrics reseted"})
