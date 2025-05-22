from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.account.factory import AccountFactory
from core.account.serializers import (
    AccountOutputSerializer,
    CreateAccountInputSerializer,
)
from core.shared.schema_exceptions import STANDARD_ERROR_RESPONSES


class AccountRegisterAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_account = AccountFactory.make_create_account()

    @extend_schema(
        tags=['Account'],
        request=CreateAccountInputSerializer,
        responses={201: AccountOutputSerializer, **STANDARD_ERROR_RESPONSES},
        summary='Register Account',
        description='Endpoint to register a new account.',
        auth=[],
    )
    def post(self, request) -> Response:
        serializer = CreateAccountInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = self.create_account.create_new_account(
            name=serializer.validated_data.get('name'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
        )

        output_data = AccountOutputSerializer(instance=account).data

        return Response(data=output_data, status=status.HTTP_201_CREATED)
