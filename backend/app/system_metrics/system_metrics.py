import asyncio

from prometheus_client import Counter, Histogram, Gauge
import psutil


REQUEST_COUNT = Counter(
    "app_requests_count",
    "Total number of requests"
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latency of requests in seconds"
)
CPU_USAGE = Gauge(
    "custom_cpu_usage_percent",
    "CPU usage percent"
)
MEMORY_USAGE = Gauge(
    "custom_memory_usage_percent",
    "Memory usage percent"
)


def record_request_data_metrics(process_time: float) -> None:
    """Записывает данные о времени обработки запроса."""
    
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(process_time)


async def update_hardware_metrics():
    """Запписывает данные о нагрузке на ЦП и ОЗУ во время работы сервиса"""

    while True:
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_usage = psutil.virtual_memory().percent
        
        CPU_USAGE.set(cpu_usage)
        MEMORY_USAGE.set(memory_usage)
        
        await asyncio.sleep(1)


def reset_metrics():
    """Сбрасывает накопленные метрики"""
    REQUEST_COUNT.clear()
    REQUEST_LATENCY.clear()
    CPU_USAGE.clear()
    MEMORY_USAGE.clear()
