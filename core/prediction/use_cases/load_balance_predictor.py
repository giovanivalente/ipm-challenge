from decimal import Decimal

from core.prediction.prediction_models.balance_predictor import BalancePredictor


class LoadBalancePredictor:

    def __init__(self, balance_predictor: BalancePredictor):
        self._balance_predictor = balance_predictor

    def load_model(self, avg_deposit: Decimal, avg_withdrawal: Decimal, current_balance: Decimal, months_ahead: int):
        input_data = [
            [
                float(avg_deposit),
                float(avg_withdrawal),
                float(current_balance),
                float(months_ahead)
            ]
        ]
        model = self._balance_predictor.load_model()
        prediction = model.predict(input_data)

        return {"future_balance": Decimal(prediction[0])}
