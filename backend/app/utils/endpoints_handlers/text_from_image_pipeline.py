import logging
import uuid

import numpy as np
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from services import image_preprocessor, text_extractor, DBWriter
from utils import init_s3_objects, DBData
from pipeline_models import TextFromFilePipelineResult


async def text_from_image_pipeline(
        request_body: BaseModel,
        image: np.ndarray,
        db_session: AsyncSession,
        logger: logging.Logger
    ) -> TextFromFilePipelineResult:
    preprocessed_image = image_preprocessor.preprocess_image(image)

    from PIL import Image
    img = Image.fromarray(preprocessed_image)
    img.save('preprocessed_image.png', quality=100)

    extracted_text = text_extractor.extract_text_from_image(preprocessed_image)
    logger.info(extracted_text)

    s3_objects = init_s3_objects(request_body, image, preprocessed_image, extracted_text)
    # s3_uploader.upload_objects(s3_objects)

    db_data = DBData(
        request_body=request_body,
        original_image_s3_url=s3_objects.original.url,
        processed_image_s3_url=s3_objects.preprocessed.url,
        extracted_text_s3_url=s3_objects.extracted_text.url,
        extracted_text=extracted_text
    )

    db_writer = DBWriter(db_session, db_data, logger)
    # await db_writer.write_all()

    # res = TextFromFilePipelineResult(extracted_text, db_writer.new_response__id)

    import uuid
    _id = str(uuid.uuid4())

    res = TextFromFilePipelineResult(extracted_text, _id)
    
    return res
