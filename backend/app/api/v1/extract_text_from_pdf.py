from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services import pdf_converter
from orm import db_engine
from validation_models import ExtractTextFromPDFRequestModel, ExtractTextFromPDFResponseModel
from utils import get_logger, text_from_pdf_pipeline, handel_error_500_exception


logger = get_logger(__name__)

router = APIRouter()


@router.post("/extract_text_from_pdf", response_model=ExtractTextFromPDFResponseModel)
@handel_error_500_exception(logger)
async def extract_text_from_pdf(
        id: str = Form(...),
        user_id: str = Form(...),
        content_type: str = Form(...),
        document_type_code: int = Form(...),
        file: UploadFile = File(...),
        db_session: AsyncSession = Depends(db_engine.get_session)
    ) -> ExtractTextFromPDFResponseModel:
    request_body = ExtractTextFromPDFRequestModel(id=id, user_id=user_id, content_type=content_type, document_type_code=document_type_code)

    images = await pdf_converter.convert_file(file)

    pipeline_result = await text_from_pdf_pipeline(request_body, images, db_session, logger)

    response = ExtractTextFromPDFResponseModel(
        request_id=request_body.id,
        response_id=pipeline_result.id,
        extracted_text=pipeline_result.extracted_text
    )

    return response
