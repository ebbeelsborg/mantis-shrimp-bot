"""
Unified response structures for consistent API responses.
"""
from rest_framework import status
from rest_framework.response import Response


def success_response(data, status_code=status.HTTP_200_OK):
    """Return a standardized success response."""
    return Response(
        {
            "success": True,
            "data": data,
        },
        status=status_code,
    )


def error_response(
    message,
    errors=None,
    error_code="ERROR",
    status_code=status.HTTP_400_BAD_REQUEST,
):
    """Return a standardized error response."""
    payload = {
        "success": False,
        "message": message,
        "error_code": error_code,
    }
    if errors:
        payload["errors"] = errors
    return Response(payload, status=status_code)
