from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc: Exception, context: dict) -> Response | None:
    response = drf_exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            return _handle_validation_error(exc, response.status_code)
        if isinstance(exc, APIException):
            return _handle_api_exception(exc, response.status_code)

    return _internal_error_response()


def _handle_validation_error(exc: ValidationError, status_code: int) -> Response:
    detail = exc.detail
    top_level_code = getattr(exc, 'code', 'VALIDATION_ERROR').upper()

    if isinstance(detail, dict):
        error_list = _format_field_errors(detail)
    elif isinstance(detail, list):
        error_list = _format_list_errors(detail)
    else:
        error_list = [{'field': None, 'message': str(detail), 'code': getattr(detail, 'code', 'invalid')}]

    return Response({'errors': [{'code': top_level_code, 'details': error_list}]}, status=status_code)


def _handle_api_exception(exc: APIException, status_code: int) -> Response:
    code = (
        getattr(exc.detail, 'code', exc.default_code).upper()
        if hasattr(exc.detail, 'code')
        else exc.default_code.upper()
    )
    return Response({'errors': [{'code': code, 'details': {'message': str(exc.detail)}}]}, status=status_code)


def _internal_error_response() -> Response:
    return Response(
        {
            'errors': [
                {
                    'code': 'INTERNAL_ERROR',
                    'details': {'message': 'An unexpected error occurred. Our team has been notified.'},
                }
            ]
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _format_field_errors(detail: dict, parent_field: str = '') -> list:
    error_list = []
    for field, errors in detail.items():
        full_field = f'{parent_field}.{field}' if parent_field else field
        if isinstance(errors, dict):
            error_list.extend(_format_field_errors(errors, full_field))
        elif isinstance(errors, list):
            for err in errors:
                error_list.append({'field': full_field, 'message': str(err), 'code': getattr(err, 'code', 'invalid')})
        else:
            error_list.append({'field': full_field, 'message': str(errors), 'code': getattr(errors, 'code', 'invalid')})
    return error_list


def _format_list_errors(errors: list) -> list:
    return [{'field': None, 'message': str(err), 'code': getattr(err, 'code', 'invalid')} for err in errors]
