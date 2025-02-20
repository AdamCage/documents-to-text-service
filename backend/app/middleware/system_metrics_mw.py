import time

from fastapi import Request

from system_metrics.system_metrics import record_request_data_metrics


async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    if request.url.path not in ("/metrics", "/reset_metrics"):
        record_request_data_metrics(process_time)
    
    return response
