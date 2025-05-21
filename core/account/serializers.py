import re

from rest_framework import serializers


class CreateAccountInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('The password should contain at least one uppercase character.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('The password should contain at least one lowercase character.')
        if not re.search(r'\d', value):
            raise serializers.ValidationError('The password should contain at least one number.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('The password should contain at least one special character.')
        return value


class AccountOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
