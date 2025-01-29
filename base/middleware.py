import logging
import time
from django.conf import settings

logger = logging.getLogger("django")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        # Log request details
        duration = time.time() - start_time
        log_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": f"{duration:.2f}s",
            "user": (
                request.user.username if request.user.is_authenticated else "anonymous"
            ),
        }

        logger.info(f"Request: {log_data}")
        return response
