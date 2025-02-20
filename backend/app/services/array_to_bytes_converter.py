import io
import logging

import numpy as np
from PIL import Image

from utils import get_logger, FileConverter, BytesConvertingError


logger = get_logger(__name__)


class ArrayToPngBytesConverter(FileConverter):
    """Класс для конвератации изображений."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger


    async def convert_file(self, file: np.ndarray) -> io.BytesIO:
        """Обработать изображение из формата np.ndarray в png и преобразовать в байты."""
        try:
            image = Image.fromarray(file)

            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")

            img_byte_arr.seek(0)

            return img_byte_arr
        
        except Exception as e:
            msg = f"Error converting array to PNG: {e}"
            self.logger.error(msg)
            raise BytesConvertingError(msg)
        

    async def convert_string(self, string: str) -> io.BytesIO:
        """Конвертировать строку в байты и вернуть в BytesIO."""
        try:
            byte_data = string.encode('utf-8')
            byte_stream = io.BytesIO(byte_data)
            byte_stream.seek(0)

            return byte_stream
        
        except Exception as e:
            msg = f"Error converting string to bytes: {e}"
            self.logger.error(msg)
            raise BytesConvertingError(msg)


bytes_converter = ArrayToPngBytesConverter(logger)
