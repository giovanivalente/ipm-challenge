from django.urls import path

from core.account.views.account_detail import AccountDetailAPIView
from core.account.views.create_account import CreateAccountAPIView

app_name = 'account'

urlpatterns = [
    path('accounts/', CreateAccountAPIView.as_view(), name='create-account'),
    path('accounts/<str:account_id>', AccountDetailAPIView.as_view(), name='account-detail'),
]
