import time
from fastapi import Request
from logger import logger

async def log_middleware(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Started - {request.method} - {request.url.path}")
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"Finished - {request.method} - {request.url.path} - status_code: {response.status_code} - duration: {formatted_process_time}ms")

    return response