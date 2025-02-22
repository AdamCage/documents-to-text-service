from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def setup_prometheus(app: FastAPI):
    """Setup Prometheus instrumentation."""
    prometheus_instrumentator = Instrumentator()
    prometheus_instrumentator.instrument(app).expose(app, endpoint="/metrics")
