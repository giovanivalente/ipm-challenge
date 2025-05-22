from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView


@extend_schema(
    tags=['Authentication'],
    summary='Get JWT Token',
    description='Endpoint to get JWT token with email and password.',
    auth=[],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass
