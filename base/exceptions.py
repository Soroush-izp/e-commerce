from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

logger = logging.getLogger("django")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        logger.error(f"Unhandled exception: {exc}")
        return Response(
            {
                "error": "Internal server error",
                "detail": (
                    str(exc) if settings.DEBUG else "An unexpected error occurred"
                ),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    logger.error(f"API error: {response.data}")
    return response
