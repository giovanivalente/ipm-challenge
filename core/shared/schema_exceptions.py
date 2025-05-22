from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers

ErrorDetailSerializer = inline_serializer(
    name='ErrorDetail',
    fields={
        'code': serializers.CharField(default='some_error_code'),
        'details': serializers.DictField(default={'message': 'Some error message.'}),
    },
)

StandardErrorSerializer = inline_serializer(
    name='StandardErrorResponse', fields={'errors': serializers.ListField(child=ErrorDetailSerializer)}
)

STANDARD_ERROR_RESPONSES = {
    400: OpenApiResponse(response=StandardErrorSerializer, description='Invalid Request.'),
    401: OpenApiResponse(
        response=StandardErrorSerializer, description='Authentication credentials were not provided or are invalid.'
    ),
    404: OpenApiResponse(response=StandardErrorSerializer, description='Not found.'),
    409: OpenApiResponse(
        response=StandardErrorSerializer, description='A resource with the given data already exists.'
    ),
    500: OpenApiResponse(response=StandardErrorSerializer, description='Unexpected internal error.'),
}
