from django.urls import path

from core.authentication.views import CustomTokenObtainPairView

app_name = 'authentication'

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
