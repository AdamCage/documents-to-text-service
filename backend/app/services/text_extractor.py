import logging

import numpy as np
from PIL import Image

from core import config
from utils import get_logger, extractor_factory, ExtractorFactory, TextExtractionError


logger = get_logger(__name__)


class TextExtractor:
    """Класс для извлечения текста из изображений с использованием OCR-моделей."""
    

    def __init__(self, extractor_factory: ExtractorFactory, logger: logging.Logger) -> None:
        """_summary_

        Args:
            extractor_factory (ExtractorFactory): _description_
            logger (logging.Logger): _description_
        """
        self.extractor = extractor_factory.create_extractor()
        self.logger = logger


    def extract_text_from_image(self, image: np.ndarray) -> str:
        """Извлечь текст из изображения.

        Args:
            image (np.ndarray): Изображение, из которого нужно извлечь текст.

        Returns:
            str: Извлеченный текст.
        """
        self.logger.info("Extracting text.")

        try:
            image = Image.fromarray(image)
            image = np.array(image)
            extracted_text = self.extractor.readtext(image)
            
            self.logger.info("Text extracted.")

        except Exception as e:
            msg = f"{self.extractor.__class__.__name__} text extracting error: {str(e)}"
            self.logger.error(msg)
            raise TextExtractionError(msg)

        return extracted_text
    

text_extractor = TextExtractor(extractor_factory, logger)
