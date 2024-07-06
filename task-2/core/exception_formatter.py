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
    401: "Unauthorized",
    403: "Forbidden",
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
            "status": STATUS_CODE_MESSAGES.get(response.status_code),
            "message": response.data.get("message", "An error occurred"),
            "statusCode": response.status_code,
        }

        response.data = custom_response_data

    return response


class ExceptionFormatter(BaseExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        print(dir(error_response.errors[0]))
        error = error_response.errors[0]

        return {
            "status": error.code,
            "message": "Registration unsuccessful",
            "statusCode": error.code,
        }
