import logging

import numpy as np
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from services import image_preprocessor, text_extractor, DBWriter
from utils import init_s3_objects, DBData
from .pipeline_models import TextFromFilePipelineResult


async def text_from_pdf_pipeline(
        request_body: BaseModel,
        images: list[np.ndarray],
        db_session: AsyncSession,
        logger: logging.Logger
    ) -> TextFromFilePipelineResult:
    texts = []

    # db_data = DBData(request_body=request_body)
    # db_writer = DBWriter(db_session, db_data, logger)
    # await db_writer.write_request()

    logger.info(f'Extracting text from {len(images) + 1} pages.')
    for i, image in enumerate(images):
        # preprocessed_image = image
        preprocessed_image = image_preprocessor.preprocess_image(image)

        from PIL import Image
        img = Image.fromarray(preprocessed_image)
        img.save(f'preprocessed_image_{i}.png', quality=100)

        extracted_text = text_extractor.extract_text_from_image(preprocessed_image)
        texts.append(extracted_text)

        # s3_objects = init_s3_objects(request_body, image, preprocessed_image, extracted_text)
        # s3_uploader.upload_objects(s3_objects)

        # db_data.image_number = i
        # db_data.original_image_s3_url = s3_objects.original.url
        # db_data.processed_image_s3_url = s3_objects.preprocessed.url
        # db_data.extracted_text_s3_url = s3_objects.extracted_text.url
        # db_data.extracted_text = extracted_text

        # await db_writer.write_extract()

        logger.info(f'Extracted text from {i} / {len(images)} pages.')
        
    full_text = "\n\n".join(texts)
    logger.info(full_text)

    # db_data.extracted_text = full_text
    # await db_writer.write_response()

    # res = TextFromFilePipelineResult(extracted_text, db_writer.new_response__id)
    
    import uuid
    _id = uuid.uuid4()

    res = TextFromFilePipelineResult(_id, full_text)
    
    return res
