"""
Custom exception handlers for consistent error responses.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """Transform DRF exceptions into unified error response format."""
    response = exception_handler(exc, context)
    if response is not None:
        custom_data = {
            "success": False,
            "message": _get_error_message(response, exc),
            "error_code": _get_error_code(response.status_code),
        }
        if hasattr(exc, "detail") and isinstance(exc.detail, dict):
            custom_data["errors"] = exc.detail
        response.data = custom_data
    else:
        response = Response(
            {
                "success": False,
                "message": "An unexpected error occurred.",
                "error_code": "SERVER_ERROR",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response


def _get_error_message(response, exc):
    """Extract human-readable message from exception."""
    if hasattr(exc, "detail"):
        if isinstance(exc.detail, list):
            return exc.detail[0] if exc.detail else "An error occurred."
        if isinstance(exc.detail, dict):
            first_key = next(iter(exc.detail), None)
            if first_key:
                val = exc.detail[first_key]
                return val[0] if isinstance(val, list) else str(val)
        return str(exc.detail)
    return "An error occurred."


def _get_error_code(status_code):
    """Map HTTP status code to error code string."""
    codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        422: "UNPROCESSABLE_ENTITY",
        429: "TOO_MANY_REQUESTS",
        500: "SERVER_ERROR",
    }
    return codes.get(status_code, "ERROR")
