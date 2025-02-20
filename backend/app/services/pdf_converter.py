import logging

import pymupdf
import numpy as np
from fastapi import UploadFile

from utils import get_logger, FileConverter, ImageConversionError


logger = get_logger(__name__)


class PDFConverter(FileConverter):
    """Класс для конвертации PDF-документов."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger


    async def convert_file(self, file: UploadFile) -> list[np.ndarray]:
        """Обработать PDF и вернуть изображения из всех страниц в формате numpy."""
        try:
            pdf_document = pymupdf.open(stream=await file.read(), filetype="pdf")

            if pdf_document.page_count == 0:
                msg = "PDF is empty"
                self.logger.error(msg)
                raise ImageConversionError(msg)

            images = []
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                pix = page.get_pixmap()
                image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                images.append(image)
        
        except Exception as e:
            msg = f"PDF-file convertation error: {str(e)}"
            self.logger.error(msg)
            raise ImageConversionError(msg)

        return images


pdf_converter = PDFConverter(logger)
