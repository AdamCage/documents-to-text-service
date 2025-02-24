from typing import Optional
from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services import image_converter
from orm import db_engine
from validation_models import ExtractTextFromImageWithLLMCorrectionRequestModel, ExtractTextFromImageWithLLMCorrectionResponseModel
from utils import get_logger, text_from_image_pipeline, llm_correction_pipeline, handel_error_500_exception


logger = get_logger(__name__)

router = APIRouter()


@router.post("/extract_text_from_image_with_llm_correction", response_model=ExtractTextFromImageWithLLMCorrectionResponseModel)
@handel_error_500_exception(logger)
async def extract_text_from_image_with_llm_correction(
        id: str = Form(...),
        user_id: str = Form(...),
        content_type: str = Form(...),
        document_type_code: int = Form(...),
        custom_prompt: Optional[str] = Form(None),
        file: UploadFile = File(...),
        db_session: AsyncSession = Depends(db_engine.get_session)
    ) -> ExtractTextFromImageWithLLMCorrectionResponseModel:
    request_body = ExtractTextFromImageWithLLMCorrectionRequestModel(
        id=id,
        user_id=user_id,
        content_type=content_type,
        document_type_code=document_type_code,
        custom_prompt=custom_prompt
    )

    image = await image_converter.convert_file(file)

    pipeline_result = await text_from_image_pipeline(request_body, image, db_session, logger)
    llm_corrected_text = await llm_correction_pipeline(pipeline_result.extracted_text, request_body.document_type_code, logger, custom_prompt)

    response = ExtractTextFromImageWithLLMCorrectionResponseModel(
        request_id=request_body.id,
        response_id=pipeline_result.id,
        extracted_text=pipeline_result.extracted_text,
        llm_corrected_text=llm_corrected_text
    )

    return response
