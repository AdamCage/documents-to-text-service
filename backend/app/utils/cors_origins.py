import logging

from dotenv import dotenv_values


class CORSOrigins:
    """Класс для управления разрешенными источниками (CORS) в зависимости от окружения."""

    def __init__(self, config: dict, logger: logging.Logger) -> None:
        self._origins = self._load_origins(config)
        self._methods = self._load_methods(config)
        self._headers = self._load_headers(config)
        self.logger = logger


    def _load_origins(self, config: dict):
        """Загружает разрешенные источники в зависимости от окружения."""
        env = config.env
        
        if env == "PROD":
            cors_origins = dotenv_values().get("CORS_ORIGINS")

            return [origin.strip() for origin in cors_origins.split(",")]

        elif env == "TEST":
            return ["*"]

        else:
            msg = 'The application environment type is incorrectly specified. It must be "PROD" or "TEST"'
            self.logger.error(msg)
            raise ValueError(msg)


    def _load_methods(self, config: dict):
        """Загружает разрешенные методы в зависимости от окружения."""
        env = config.env
        
        if env == "PROD":
            methods = dotenv_values().get("CORS_METHODS")
            return [method.strip() for method in methods.split(",")]
        
        elif env == "TEST":
            return ["*"]
        
        else:
            return []


    def _load_headers(self, config: dict):
        """Загружает разрешенные заголовки в зависимости от окружения."""
        env = config.env
        
        if env == "PROD":
            headers = dotenv_values().get("CORS_HEADERS", "*")
            return [header.strip() for header in headers].split(",")
        
        elif env == "TEST":
            return ["*"]
        
        else:
            return []


    @property
    def origins(self):
        """Возвращает список разрешенных источников."""
        return self._origins


    @origins.setter
    def origins(self, new_origins):
        """Устанавливает новый список разрешенных источников."""
        if isinstance(new_origins, list):
            self._origins = new_origins

        else:
            raise ValueError("origins must be a list of strings.")


    @property
    def methods(self):
        """Возвращает список разрешенных методов."""
        return self._methods
    

    @methods.setter
    def methods(self, new_methods):
        """Устанавливает новый список разрешенных методов."""
        if isinstance(new_methods, list):
            self._methods = new_methods

        else:
            raise ValueError("methods must be a list of strings.")


    @property
    def headers(self):
        """Возвращает список разрешенных заголовков."""
        return self._headers


    @headers.setter
    def methods(self, new_headers):
        """Устанавливает новый список разрешенных методов."""
        if isinstance(new_headers, list):
            self._headers = new_headers

        else:
            raise ValueError("headers must be a list of strings.")
