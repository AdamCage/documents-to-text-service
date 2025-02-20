from abc import ABC, abstractmethod

import numpy as np


class OcrReader(ABC):
    """Абстрактный класс для считывания текста с изображения."""
    
    @abstractmethod
    def readtext(self, image: np.ndarray) -> str:
        pass
