from django.core.cache import cache
from functools import wraps
import hashlib
from rest_framework.exceptions import ValidationError
from typing import Any, Callable, Optional, Union, Dict
from django.http import HttpRequest, HttpResponse


def cache_response(timeout: int = 300) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(
            self: Any, request: HttpRequest, *args: Any, **kwargs: Any
        ) -> HttpResponse:
            # Create a cache key based on the request
            key_parts = [
                request.path,
                str(request.user.pk if request.user.is_authenticated else "anonymous"),
                str(request.query_params),
            ]
            cache_key = hashlib.md5("".join(key_parts).encode()).hexdigest()

            # Try to get the response from cache
            response = cache.get(cache_key)
            if response is not None:
                return response

            # Generate the response
            response = view_func(self, request, *args, **kwargs)

            # Cache the response
            cache.set(cache_key, response, timeout)
            return response

        return wrapper

    return decorator


def validate_file_size(file_obj: Any, max_size_mb: int = 5) -> None:
    """Validate file size."""
    if file_obj.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size must not exceed {max_size_mb}MB")
