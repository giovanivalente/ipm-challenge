from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.account.mapper import account_entity_to_model
from core.account.tests.factory import AccountModelFactory


class TestGetAccount:
    def setup_method(self):
        self.client = APIClient()
        self.account = AccountModelFactory.create(as_entity=True)
        self.url = reverse('account:account-detail', args=[self.account.id])

    @pytest.fixture
    def authenticate(self):
        self.client.force_authenticate(user=account_entity_to_model(self.account))

    @pytest.mark.django_db
    def test_should_return_an_account(self, authenticate):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(self.account.id)

    @pytest.mark.django_db
    def test_should_return_not_authenticated(self):
        response = self.client.get(self.url)

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert expected_message_error == 'Authentication credentials were not provided.'


    @pytest.mark.django_db
    def test_should_raise_error_when_account_id_is_not_a_valid_uuid(self, authenticate):
        url = reverse('account:account-detail', args=['uuid_invalid_format'])

        response = self.client.get(url)

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'Account ID is not a valid UUID.'

    @pytest.mark.django_db
    def test_should_parse_str_id_to_uuid(self, authenticate):
        url = reverse('account:account-detail', args=[str(self.account.id)])

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(self.account.id)

    @pytest.mark.django_db
    def test_should_raise_error_when_account_id_is_not_found(self, authenticate):
        url = reverse('account:account-detail', args=[uuid4()])

        response = self.client.get(url)

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert expected_message_error == 'Account not found.'
