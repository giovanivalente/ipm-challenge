from django.urls import path

from core.prediction.views.balance_predictor import BalancePredictionAPIView

app_name = 'prediction'

urlpatterns = [
    path("prediction/balance/", BalancePredictionAPIView.as_view(), name="balance-prediction"),
]