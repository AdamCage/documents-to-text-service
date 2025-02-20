from typing import Any

from core import config
from ocr_wrappers import get_tesseract_reader, get_easy_ocr_reader


class ExtractorFactory:
    """Фабрика для создания экземпляров текстовых извлекателей."""

    @staticmethod
    def create_extractor() -> Any:
        """Создает и возвращает экземпляр текстового извлекателя в зависимости от конфигурации.

        Returns:
            Any: Экземпляр текстового извлекателя.
        """
        framework = config.model.get("framework")

        if framework == "easyocr":
            return get_easy_ocr_reader(config.model)
        
        elif framework == "tesseract":
            return get_tesseract_reader(config.model)
        
        # elif framework == "for_future_extensions":
        #     pass

        else:
            raise ValueError(f"Unsupported framework: {framework}")


extractor_factory = ExtractorFactory()
