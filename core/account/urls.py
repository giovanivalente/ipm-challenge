from django.urls import path

from core.account.views.account_detail import AccountDetailAPIView
from core.account.views.account_register import AccountRegisterAPIView

app_name = 'account'

urlpatterns = [
    path('accounts/register/', AccountRegisterAPIView.as_view(), name='account-register'),
    path('accounts/', AccountDetailAPIView.as_view(), name='account-detail'),
]
