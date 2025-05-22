from django.urls import path

from core.account.views.account_detail import AccountDetailAPIView

app_name = 'account'

urlpatterns = [
    path('accounts/', AccountDetailAPIView.as_view(), name='account-detail'),
]
