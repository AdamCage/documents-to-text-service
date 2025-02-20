class ImageConversionError(Exception):
    """Кастомное исключение для ошибок конвертации изображений."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ImagePreprocessorError(Exception):
    """Кастомное исключение для ошибок предобработки изображений."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TextExtractionError(Exception):
    """Кастомное исключение для ошибок предобработки изображений."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class S3UploadingError(Exception):
    """Кастомное исключение для ошибок загрузки объектов в S3."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BytesConvertingError(Exception):
    """Кастомное исключение для ошибок перевода объектов в байты"""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DataBaseWritingError(Exception):
    """Кастомное исключение для ошибок записи данных в БД"""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message