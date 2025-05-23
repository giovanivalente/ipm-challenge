from decimal import Decimal
from unittest.mock import Mock

import pytest
from sklearn.linear_model import LinearRegression

from core.prediction.factory import PredictionFactory


class TestLoadModel:
    @pytest.fixture
    def sut(self):
        sut = PredictionFactory.make_load_balance_predictor()
        sut._balance_predictor.load_model = Mock(return_value=self.model)
        return sut

    def setup_method(self):
        self.model = Mock(spec=LinearRegression)
        self.model.predict = Mock(return_value=[100])
        self.avg_deposit = Decimal(100)
        self.avg_withdrawal = Decimal(80)
        self.current_balance = Decimal(340)
        self.months_ahead = 3

    def test_should_call_load_model_with_correct_params(self, sut):
        sut.load_model(
            avg_deposit=self.avg_deposit,
            avg_withdrawal=self.avg_withdrawal,
            current_balance=self.current_balance,
            months_ahead=self.months_ahead,
        )

        sut._balance_predictor.load_model.assert_called_once_with()

    def test_should_call_predict_with_correct_params(self, sut):
        input_data = [
            [float(self.avg_deposit), float(self.avg_withdrawal), float(self.current_balance), float(self.months_ahead)]
        ]

        sut.load_model(
            avg_deposit=self.avg_deposit,
            avg_withdrawal=self.avg_withdrawal,
            current_balance=self.current_balance,
            months_ahead=self.months_ahead,
        )

        sut._balance_predictor.load_model.return_value.predict.assert_called_once_with(input_data)

    def test_should_return_successful_response(self, sut):
        response = sut.load_model(
            avg_deposit=self.avg_deposit,
            avg_withdrawal=self.avg_withdrawal,
            current_balance=self.current_balance,
            months_ahead=self.months_ahead,
        )

        assert response == {'future_balance': Decimal(100)}
