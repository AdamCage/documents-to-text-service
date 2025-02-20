import logging

import numpy as np

from utils import get_logger, ImagePreprocessorError, ContrastEnhancer, \
    GrayscaleConverter, Denoiser, AdaptiveBinarizer, AutoCropper, SharpnessEnhancer, \
        SharpnessEnhancer, RotationCorrector

logger = get_logger(__name__)


class ImagePreprocessor:
    """Класс для предварительной обработки изображений."""
    
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.processors = [
            # AutoCropper(),
            RotationCorrector(),
            GrayscaleConverter()
        ]


    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Предварительная обработка изображения."""
        for processor in self.processors:
            try:
                image = processor.process(image)
                self.logger.info(f"Processed with {processor.__class__.__name__}")

            except Exception as e:
                msg = f"{processor.__class__.__name__} processing error: {str(e)}"
                self.logger.error(msg)
                raise ImagePreprocessorError(msg)

        self.logger.info(f"Image is preprocessed")

        return image


image_preprocessor = ImagePreprocessor(logger)
