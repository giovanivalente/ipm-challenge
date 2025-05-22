from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.account.factory import AccountFactory
from core.account.serializers import (
    AccountOutputSerializer,
    CreateAccountInputSerializer,
)


class AccountRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_account = AccountFactory.make_create_account()

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
