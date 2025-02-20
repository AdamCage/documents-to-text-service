from abc import ABC, abstractmethod

import numpy as np


class ImageProcessor(ABC):
    """Абстрактный класс для обработки изображений."""
    
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """Обработать изображение."""
        pass
