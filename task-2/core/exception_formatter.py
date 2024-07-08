from drf_standardized_errors.formatter import (
    ExceptionFormatter as BaseExceptionFormatter,
)
from drf_standardized_errors.types import ErrorResponse


from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.exceptions import ValidationError
from drf_standardized_errors.handler import (
    exception_handler as standardized_exception_handler,
)

STATUS_CODE_MESSAGES = {
    400: "Bad request",
    401: "Authentication failed",
    403: "Bad request",
    405: "Method not allowed",
    404: "Not found",
    500: "Internal server error",
}


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        errors = [
            {"field": key, "message": value[0]} for key, value in response.data.items()
        ]

        response.data = {"errors": errors}
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        response = standardized_exception_handler(exc, context)
        custom_response_data = {
            "status": "Bad request",
            "message": response.data.get(
                "message", STATUS_CODE_MESSAGES.get(response.status_code)
            ),
            "statusCode": response.status_code,
        }

        response.data = custom_response_data

    return response
