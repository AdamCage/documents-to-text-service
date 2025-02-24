from .setup_cors import *
from .setup_middlewares import *
from .setup_prometeus import *
from .setup_routes import *
from .setup_logger import *


__all__ = [
    "setup_prometheus",
    "setup_middlewares",
    "setup_routes",
    "setup_cors",
    "setup_logger"
]
