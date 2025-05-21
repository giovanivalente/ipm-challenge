from django.urls import path

from core.account.views.create_list_account import AccountCreateListAPIView

app_name = 'account'

urlpatterns = [
    path('accounts/', AccountCreateListAPIView.as_view(), name='account-create-list'),
]
