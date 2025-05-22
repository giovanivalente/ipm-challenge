from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.account.factory import AccountFactory
from core.account.serializers import (
    AccountOutputSerializer,
    UpdateAccountInputSerializer,
)


class AccountDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_get_account = AccountFactory.make_db_get_account()
        self.update_account = AccountFactory.make_update_account()
        self.delete_account = AccountFactory.make_delete_account()

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
