import easyocr

from utils import OcrReader


class EasyOCRModelConfiguration:
    """Класс для хранения конфигурации OCR-модели."""

    def __init__(self, config: dict) -> None:
        self.init_params = config["init_params"]
        self.readtext_params = config["readtext_params"]


class EasyOCRWrapper(OcrReader):
    def __init__(self, config: EasyOCRModelConfiguration):
        self.config = config
        self.reader = easyocr.Reader(**config.init_params)


    def readtext(self, image) -> str:
        results = self.reader.readtext(image, **self.config.readtext_params)
        extracted_text = " ".join([result[1] for result in results])

        return extracted_text


def get_easy_ocr_reader(model_config: dict) -> OcrReader:
    """Фабричный метод для получения экземпляра EasyOCR-ридера."""
    config = EasyOCRModelConfiguration(model_config)
    
    return EasyOCRWrapper(config)
