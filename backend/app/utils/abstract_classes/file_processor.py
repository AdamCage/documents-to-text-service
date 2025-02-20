from abc import ABC, abstractmethod

from fastapi import UploadFile
import numpy as np


class FileConverter(ABC):
    """Абстрактный класс для конвертации файлов."""
    
    @abstractmethod
    async def convert_file(self, file: UploadFile | np.ndarray) -> np.ndarray | list[np.ndarray]:
        """Сконвертировать загруженный файл и вернуть результат."""
        pass
