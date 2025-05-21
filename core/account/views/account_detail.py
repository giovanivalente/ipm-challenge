from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.account.factory import AccountFactory
from core.account.serializers import AccountIdInputSerializer, AccountOutputSerializer


class AccountDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_get_account = AccountFactory.make_db_get_account()

    def get(self, request, account_id: str) -> Response:
        serializer = AccountIdInputSerializer(data={'account_id': account_id})
        serializer.is_valid(raise_exception=True)

        account = self.db_get_account.get_by_id(account_id=serializer.validated_data['account_id'])

        output_data = AccountOutputSerializer(instance=account).data

        return Response(data=output_data, status=status.HTTP_200_OK)

    def patch(self, request, account_id: str) -> Response:
        # serializer = AccountIdInputSerializer(data={'account_id': account_id})
        # serializer.is_valid(raise_exception=True)
        # account_id = serializer.validated_data['account_id']
        #
        # serializer = UpdateAccountInputSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        return Response(status=200)
