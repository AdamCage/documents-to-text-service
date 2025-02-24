from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services import image_converter
from orm import db_engine
from validation_models import ExtractTextFromImageRequestModel, ExtractTextFromImageResponseModel
from utils import get_logger, text_from_image_pipeline, handel_error_500_exception


logger = get_logger(__name__)

router = APIRouter()


@router.post("/extract_text_from_image", response_model=ExtractTextFromImageResponseModel)
@handel_error_500_exception(logger)
async def extract_text_from_image(
        id: str = Form(...),
        user_id: str = Form(...),
        content_type: str = Form(...),
        document_type_code: int = Form(...),
        file: UploadFile = File(...),
        db_session: AsyncSession = Depends(db_engine.get_session)
    ) -> ExtractTextFromImageResponseModel:
    request_body = ExtractTextFromImageRequestModel(id=id, user_id=user_id, content_type=content_type, document_type_code=document_type_code)
    image = await image_converter.convert_file(file)

    pipeline_result = await text_from_image_pipeline(request_body, image, db_session, logger)

    response = ExtractTextFromImageResponseModel(
        request_id=request_body.id,
        response_id=pipeline_result.id,
        extracted_text=pipeline_result.extracted_text
    )

    return response
    