from core.prediction.prediction_models.balance_predictor import BalancePredictor
from core.prediction.use_cases.load_balance_predictor import LoadBalancePredictor


class PredictionFactory:
    @classmethod
    def make_balance_predictor(cls) -> BalancePredictor:
        return BalancePredictor()

    @classmethod
    def make_load_balance_predictor(cls) -> LoadBalancePredictor:
        return LoadBalancePredictor(balance_predictor=cls.make_balance_predictor())
