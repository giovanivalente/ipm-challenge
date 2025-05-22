import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.account.mapper import account_entity_to_model
from core.account.tests.factory import AccountModelFactory


class TestUpdateAccount:
    def setup_method(self):
        self.client = APIClient()
        self.account = AccountModelFactory.create()
        self.url = reverse('account:account-detail')

    @pytest.fixture
    def authenticate(self):
        self.client.force_authenticate(user=account_entity_to_model(self.account))

    def input_data(self):
        return {
            'name': 'client name',
            'is_active': False,
            'password': 'NewPassword@123',
            'current_password': 'Password@123',
        }

    @pytest.mark.django_db
    def test_should_update_an_account(self, authenticate):
        response = self.client.patch(self.url, data=self.input_data(), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] != self.account.name
        assert response.data['is_active'] != self.account.is_active

    @pytest.mark.django_db
    def test_should_return_not_authenticated(self):
        response = self.client.patch(self.url, data=self.input_data(), format='json')

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert expected_message_error == 'Authentication credentials were not provided.'

    @pytest.mark.django_db
    def test_should_raise_error_when_password_is_provided_and_current_password_not(self, authenticate):
        payload = self.input_data()
        del payload['current_password']

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'You must provide the current password.'

    @pytest.mark.django_db
    def test_should_raise_error_when_current_password_is_provided_and_password_not(self, authenticate):
        payload = self.input_data()
        del payload['password']

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'You must provide the new password.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_uppercase_character(self, authenticate):
        payload = self.input_data()
        payload['password'] = 'password@123'

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The password should contain at least one uppercase character.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_lowercase_character(self, authenticate):
        payload = self.input_data()
        payload['password'] = 'PASSWORD@123'

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The password should contain at least one lowercase character.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_number(self, authenticate):
        payload = self.input_data()
        payload['password'] = 'Password@'

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The password should contain at least one number.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_special_character(self, authenticate):
        payload = self.input_data()
        payload['password'] = 'Password123'

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The password should contain at least one special character.'

    @pytest.mark.django_db
    def test_should_raise_error_when_current_password_is_invalid(self, authenticate):
        payload = self.input_data()
        payload['current_password'] = 'wrong_password'

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The provided current password is invalid.'

    @pytest.mark.django_db
    def test_should_raise_error_when_current_password_is_invalid(self, authenticate):
        payload = self.input_data()
        payload['current_password'] = 'wrong_password'

        response = self.client.patch(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The provided current password is invalid.'
