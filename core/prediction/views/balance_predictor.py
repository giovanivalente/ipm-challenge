from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.prediction.factory import PredictionFactory
from core.prediction.serializers import BalanceInputSerializer, BalanceOutputSerializer
from core.shared.schema_exceptions import STANDARD_ERROR_RESPONSES


class BalancePredictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_balance_predictor = PredictionFactory.make_load_balance_predictor()

    @extend_schema(
        tags=['Prediction'],
        request=BalanceInputSerializer,
        responses={200: BalanceOutputSerializer, **STANDARD_ERROR_RESPONSES},
        summary='Prediction Balance',
        description='Predict future balance.',
    )
    def post(self, request) -> Response:
        serializer = BalanceInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prediction = self.load_balance_predictor.load_model(**serializer.validated_data)

        output_data = BalanceOutputSerializer(instance=prediction).data

        return Response(data=output_data, status=status.HTTP_200_OK)
