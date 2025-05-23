import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import settings
from core.account.mapper import account_entity_to_model
from core.account.models import AccountModel
from core.account.tests.factory import AccountModelFactory
from core.prediction.prediction_models.balance_predictor import BalancePredictor


class TestBalancePrediction:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('prediction:balance-prediction')
        self.account = AccountModelFactory.create(as_entity=True)

    @pytest.fixture
    def authenticate(self):
        self.client.force_authenticate(user=account_entity_to_model(self.account))

    def input_data(self):
        return {'avg_deposit': 240, 'avg_withdrawal': 144, 'current_balance': 100, 'months_ahead': 3}

    def remove_existing_model_file(self):
        path = settings.BALANCE_MODEL_PATH
        if path.exists():
            path.unlink()

    def create_model_file(self):
        path = settings.BALANCE_MODEL_PATH
        if not path.exists():
            BalancePredictor().load_model()

    @pytest.mark.django_db
    def test_should_return_new_prediction(self, authenticate):
        self.remove_existing_model_file()

        response = self.client.post(self.url[:-1], data=self.input_data(), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'future_balance' in response.data

    @pytest.mark.django_db
    def test_should_return_existing_prediction(self, authenticate):
        self.create_model_file()

        response = self.client.post(self.url, data=self.input_data(), format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'future_balance' in response.data

    @pytest.mark.django_db
    def test_should_return_not_authenticated(self):
        response = self.client.post(self.url, data=self.input_data(), format='json')

        expected_message_error = response.data['errors'][0]['details']['message']

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert expected_message_error == 'Authentication credentials were not provided.'

    @pytest.mark.django_db
    def test_should_raise_error_when_avg_deposit_is_not_provided(self, authenticate):
        payload = self.input_data()
        del payload['avg_deposit']

        response = self.client.post(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'This field is required.'

    @pytest.mark.django_db
    def test_should_raise_error_when_avg_withdrawal_is_not_provided(self, authenticate):
        payload = self.input_data()
        del payload['avg_withdrawal']

        response = self.client.post(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'This field is required.'

    @pytest.mark.django_db
    def test_should_raise_error_when_current_balance_is_not_provided(self, authenticate):
        payload = self.input_data()
        del payload['current_balance']

        response = self.client.post(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'This field is required.'

    @pytest.mark.django_db
    def test_should_raise_error_when_months_ahead_is_not_provided(self, authenticate):
        payload = self.input_data()
        del payload['months_ahead']

        response = self.client.post(self.url, data=payload, format='json')

        expected_message_error = response.data['errors'][0]['details'][0]['message']

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'This field is required.'
