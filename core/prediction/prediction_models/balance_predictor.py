import logging
import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

from core import settings

logger = logging.getLogger(__name__)


class BalancePredictor:

    def __init__(self, model_path: Path = None):
        self.model_path = model_path or settings.BALANCE_MODEL_PATH

    def load_model(self) -> LinearRegression:
        try:
            if self.model_path.exists():
                model = joblib.load(self.model_path)
                logger.info('Loading balance model.')

                return model
        except Exception as exc:
            logger.warning(f'Error loading the Balance Model, we will train a new one. Error: {exc}')

        return self._train_new_model()

    def _train_new_model(self) -> LinearRegression:
        # [avg_deposit, avg_withdrawal, current_balance, months_ahead]
        features = np.array(
            [
                [1000, 800, 500, 1],
                [1200, 700, 600, 2],
                [800, 900, 400, 3],
                [1500, 1000, 300, 6],
            ]
        )
        target = np.array([700, 1100, 200, 800])

        model = LinearRegression()
        model.fit(features, target)

        logger.info('Training balance model.')
        self._save_model(model)

        return model

    def _save_model(self, model: LinearRegression) -> None:
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(model, self.model_path)

        logger.info('Trained balance model was saved.')
