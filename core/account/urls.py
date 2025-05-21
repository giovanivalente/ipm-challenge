from django.urls import path

from core.account.views.create_account import CreateAccountAPIView

app_name = 'account'

urlpatterns = [
    path('accounts/', CreateAccountAPIView.as_view(), name='create-account'),
]
