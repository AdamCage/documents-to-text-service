from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services import image_converter, image_preprocessor, text_extractor, s3_uploader, pdf_converter, DBWriter
from orm import db_engine
from validation_models import *
from system_metrics import reset_metrics
from utils import get_logger, init_s3_objects, DBData


logger = get_logger(__name__)

router = APIRouter()


@router.post("/extract_text_from_image", response_model=ExtractTextFromImageResponseModel)
async def extract_text_from_image(
        id: str = Form(...),
        user_id: str = Form(...),
        content_type: str = Form(...),
        file: UploadFile = File(...),
        db_session: AsyncSession = Depends(db_engine.get_session)
    ) -> ExtractTextFromImageResponseModel:
    try:
        request_body = ExtractTextFromImageRequestModel(id=id, user_id=user_id, content_type=content_type)

        image = await image_converter.convert_file(file)
        preprocessed_image = image_preprocessor.preprocess_image(image)

        from PIL import Image
        img = Image.fromarray(preprocessed_image)
        img.save('preprocessed_image.png', quality=100)

        extracted_text = text_extractor.extract_text_from_image(preprocessed_image)

        # s3_objects = init_s3_objects(request_body, image, preprocessed_image, extracted_text)
        # s3_uploader.upload_objects(s3_objects)

        # db_data = DBData(
        #     request_body=request_body,
        #     original_image_s3_url=s3_objects.original.url,
        #     processed_image_s3_url=s3_objects.preprocessed.url,
        #     extracted_text_s3_url=s3_objects.extracted_text.url,
        #     extracted_text=extracted_text
        # )
        # db_writer = DBWriter(db_session, db_data, logger)
        # await db_writer.write_all()

        import uuid
        _id = str(uuid.uuid4())

        logger.info(extracted_text)

        return ExtractTextFromImageResponseModel(
            request_id=request_body.id,
            # response_id=db_writer.new_response__id,
            response_id=_id,
            extracted_text=extracted_text
        )

    except Exception as e:
        msg = str(e)
        logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)
    

@router.post("/extract_text_from_pdf", response_model=ExtractTextFromPDFResponseModel)
async def extract_text_from_pdf(
        id: str = Form(...),
        user_id: str = Form(...),
        content_type: str = Form(...),
        file: UploadFile = File(...),
        db_session: AsyncSession = Depends(db_engine.get_session)
    ) -> ExtractTextFromPDFResponseModel:
    try:
        request_body = ExtractTextFromPDFRequestModel(id=id, user_id=user_id, content_type=content_type)

        images = await pdf_converter.convert_file(file)
        texts = []

        # db_data = DBData(request_body=request_body)
        # db_writer = DBWriter(db_session, db_data, logger)
        # await db_writer.write_request()

        logger.info(f'Extracting text from {len(images)} pages.')
        for i, image in enumerate(images):
            preprocessed_image = image_preprocessor.preprocess_image(image)

            from PIL import Image
            img = Image.fromarray(preprocessed_image)
            img.save(f'preprocessed_image_{i}.png', quality=100)

            extracted_text = text_extractor.extract_text_from_image(preprocessed_image)

            texts.append(extracted_text)

            # s3_objects = init_s3_objects(request_body, image, preprocessed_image, extracted_text)
            # s3_uploader.upload_objects(s3_objects)

            # db_data.original_image_s3_url = s3_objects.original.url
            # db_data.processed_image_s3_url = s3_objects.preprocessed.url
            # db_data.extracted_text_s3_url = s3_objects.extracted_text.url
            # db_data.extracted_text = extracted_text

            # await db_writer.write_extract()
            logger.info(f'Extracted text from {i} / {len(images)} pages.')

        full_text = "\n\n".join(texts)
        # db_data.extracted_text = full_text

        # await db_writer.write_response()

        logger.info(full_text)

        import uuid
        _id = str(uuid.uuid4())

        return ExtractTextFromPDFResponseModel(
            request_id=request_body.id,
            # response_id=db_writer.new_response__id,
            response_id=_id,
            extracted_text=full_text
        )

    except Exception as e:
        msg = str(e)
        logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/health")
def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@router.get("/reset_metrics")
def reset_metrics() -> JSONResponse:
    reset_metrics()
    return JSONResponse(content={"message": "metrics reseted"})
