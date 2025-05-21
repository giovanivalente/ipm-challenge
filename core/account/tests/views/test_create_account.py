import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.account.models import AccountModel


class TestCreateAccount:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('account:account-create-list')

    def input_data(self):
        return {'name': 'client name', 'email': 'testemail@email.com', 'password': 'Password@123'}

    @pytest.mark.django_db
    def test_should_create_new_account(self):
        payload = self.input_data()

        response = self.client.post(self.url, data=payload, format='json')

        account = AccountModel.objects.get(email=payload['email'])

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == payload['email']
        assert response.data['id'] == str(account.id)

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_name_is_not_provided(self):
        payload = self.input_data()
        del payload['name']

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'][0].code == 'required'
        assert str(response.data['name'][0]) == 'This field is required.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_email_is_not_provided(self):
        payload = self.input_data()
        del payload['email']

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'][0].code == 'required'
        assert str(response.data['email'][0]) == 'This field is required.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_is_not_provided(self):
        payload = self.input_data()
        del payload['password']

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0].code == 'required'
        assert str(response.data['password'][0]) == 'This field is required.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_uppercase_character(self):
        payload = self.input_data()
        payload['password'] = 'password@123'

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0].code == 'invalid'
        assert str(response.data['password'][0]) == 'The password should contain at least one uppercase character.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_lowercase_character(self):
        payload = self.input_data()
        payload['password'] = 'PASSWORD@123'

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0].code == 'invalid'
        assert str(response.data['password'][0]) == 'The password should contain at least one lowercase character.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_number(self):
        payload = self.input_data()
        payload['password'] = 'Password@'

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0].code == 'invalid'
        assert str(response.data['password'][0]) == 'The password should contain at least one number.'

    @pytest.mark.django_db
    def test_should_raise_validation_error_when_password_do_not_contain_one_special_character(self):
        payload = self.input_data()
        payload['password'] = 'Password123'

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0].code == 'invalid'
        assert str(response.data['password'][0]) == 'The password should contain at least one special character.'

    @pytest.mark.django_db
    def test_should_raise_error_when_account_already_exists(self):
        payload = self.input_data()

        AccountModel.objects.create(**payload)

        response = self.client.post(self.url, data=payload, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data['detail'].code == 'error'
        assert str(response.data['detail']) == 'An account with this email already exists.'
