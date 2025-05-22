from rest_framework import serializers

from core.shared.validators import validate_password


class CreateAccountInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True, validators=[validate_password])


class AccountOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class UpdateAccountInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    is_active = serializers.BooleanField(required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(min_length=8, write_only=True, required=False, validators=[validate_password])

    def validate(self, data):
        password = data.get('password')
        current_password = data.get('current_password')

        if password:
            if not current_password:
                raise serializers.ValidationError({'current_password': 'You must provide the current password.'})

        if current_password and not password:
            raise serializers.ValidationError({'password': 'You must provide the new password.'})

        return data
