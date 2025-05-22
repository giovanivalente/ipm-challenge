from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.account.factory import AccountFactory
from core.account.serializers import (
    AccountOutputSerializer,
    CreateAccountInputSerializer,
    UpdateAccountInputSerializer,
)


class AccountDetailAPIView(APIView):
    def get_permissions(self):
        return [permissions.AllowAny()] if self.request.method == 'POST' else [permissions.IsAuthenticated()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_account = AccountFactory.make_create_account()
        self.db_get_account = AccountFactory.make_db_get_account()
        self.update_account = AccountFactory.make_update_account()
        self.delete_account = AccountFactory.make_delete_account()

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

    def get(self, request) -> Response:
        account = self.db_get_account.get_by_id(account_id=request.user.id)

        output_data = AccountOutputSerializer(instance=account).data

        return Response(data=output_data, status=status.HTTP_200_OK)

    def patch(self, request) -> Response:
        account_id = request.user.id
        serializer = UpdateAccountInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_account = self.update_account.update(account_id, **serializer.validated_data)

        output_data = AccountOutputSerializer(instance=updated_account).data

        return Response(data=output_data, status=status.HTTP_200_OK)

    def delete(self, request) -> Response:
        self.delete_account.delete(account_id=request.user.id)

        return Response(status=status.HTTP_204_NO_CONTENT)
