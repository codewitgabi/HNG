from drf_standardized_errors.formatter import (
    ExceptionFormatter as BaseExceptionFormatter,
)
from drf_standardized_errors.types import ErrorResponse


class ExceptionFormatter(BaseExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        print(error_response.type)
        errors = [
            {"field": error.attr, "message": error.detail}
            for error in error_response.errors
        ]

        return {"errors": errors}
