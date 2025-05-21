from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.account.factory import AccountFactory
from core.account.serializers import AccountOutputSerializer, CreateAccountInputSerializer


class AccountCreateListAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_factory = AccountFactory.make_create_account()

    def post(self, request) -> Response:
        serializer = CreateAccountInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = self.account_factory.create_new_account(
            name=serializer.validated_data.get('name'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
        )

        output_data = AccountOutputSerializer(instance=account).data

        return Response(data=output_data, status=status.HTTP_201_CREATED)
