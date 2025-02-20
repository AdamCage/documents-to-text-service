import pytesseract
from pytesseract import image_to_string

from utils import OcrReader


class TesseractModelConfiguration:
    """Класс для хранения конфигурации OCR-модели."""

    def __init__(self, config: dict) -> None:
        self.tesseract_cmd = config["model_uri"]
        self.language = config["languages"]
        self.psm_mode = config["psm_mode"]


    def configure(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
    

class TesseractOcrWrapper(OcrReader):
    def __init__(self, config: TesseractModelConfiguration):
        config.configure()

        self.language = config.language
        self.psm_mode = config.psm_mode


    def readtext(self, image) -> str:
        tesseract_config = f"--psm {self.psm_mode}"
        return image_to_string(image, lang=self.language, config=tesseract_config)


def get_tesseract_reader(model_config: dict) -> OcrReader:
    """Фабричный метод для получения экземпляра Tesseract-ридера."""
    config = TesseractModelConfiguration(model_config)
    
    return TesseractOcrWrapper(config)
