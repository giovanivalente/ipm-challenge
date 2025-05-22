from rest_framework import serializers


class BalanceInputSerializer(serializers.Serializer):
    avg_deposit = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    avg_withdrawal = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    current_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    months_ahead = serializers.IntegerField(min_value=1)


class BalanceOutputSerializer(serializers.Serializer):
    future_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
