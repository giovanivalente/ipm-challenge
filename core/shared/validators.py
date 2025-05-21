import re

from rest_framework import serializers


def validate_password(password):
    if not re.search(r'[A-Z]', password):
        raise serializers.ValidationError('The password should contain at least one uppercase character.')
    if not re.search(r'[a-z]', password):
        raise serializers.ValidationError('The password should contain at least one lowercase character.')
    if not re.search(r'\d', password):
        raise serializers.ValidationError('The password should contain at least one number.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise serializers.ValidationError('The password should contain at least one special character.')
    return password
