import logging
import time
from fastapi import Request
from app.config import settings

logging.basicConfig(
    level=logging.INFO,
    filename="access.log",
    format="%(asctime)s - %(message)s",
)

def setup_logging(app):
    if settings.DEBUG:
        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            log_msg = f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}ms"
            logging.info(log_msg)
            return response
