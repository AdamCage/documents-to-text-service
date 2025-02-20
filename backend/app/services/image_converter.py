from io import BytesIO
import logging

import numpy as np
from PIL import Image
from fastapi import UploadFile

from utils import get_logger, FileConverter, ImageConversionError


logger = get_logger(__name__)


class ImageConverter(FileConverter):
    """Класс для конвератации изображений."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger


    async def convert_file(self, file: UploadFile) -> np.ndarray:
        """Обработать изображение и вернуть его в формате numpy."""
        try:
            content = await file.read()
            image = Image.open(BytesIO(content))
            image = np.array(image)

            if image is None:
                raise ImageConversionError("Could not decode image")

        except Exception as e:
            msg = f"Image convertation error: {str(e)}"
            self.logger.error(msg)
            raise ImageConversionError(msg)
        
        return image


image_converter = ImageConverter(logger)
