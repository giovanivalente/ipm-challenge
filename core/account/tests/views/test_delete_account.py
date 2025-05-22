import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.account.mapper import account_entity_to_model
from core.account.models import AccountModel
from core.account.tests.factory import AccountModelFactory


class TestDeleteAccount:
    def setup_method(self):
        self.client = APIClient()
        self.account = AccountModelFactory.create(as_entity=True)
        self.url = reverse('account:account-detail')

    @pytest.fixture
    def authenticate(self):
        self.client.force_authenticate(user=account_entity_to_model(self.account))

    @pytest.mark.django_db
    def test_should_delete_an_account(self, authenticate):
        account_count_before_delete = AccountModel.objects.all().count()

        response = self.client.delete(self.url)

        account_count_after_delete = AccountModel.objects.all().count()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert account_count_after_delete < account_count_before_delete
        assert not response.data

    @pytest.mark.django_db
    def test_should_return_not_authenticated(self):
        response = self.client.delete(self.url)

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert expected_message_error == 'Authentication credentials were not provided.'
