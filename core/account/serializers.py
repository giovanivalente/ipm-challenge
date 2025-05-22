from rest_framework import serializers

from core.shared.validators import validate_password


class CreateAccountInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        validators=[validate_password],
        help_text=(
            'The password should contain at least 8 characters, including letters, numbers and special characters.'
        ),
    )


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
    current_password = serializers.CharField(
        write_only=True, required=False, help_text='Required if password is provided.'
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        validators=[validate_password],
        required=False,
        help_text=(
            'Required if current_password is provided.',
            'The password should contain at least 8 characters, including letters, numbers and special characters.',
        ),
    )

    def validate(self, data):
        password = data.get('password')
        current_password = data.get('current_password')

        if password:
            if not current_password:
                raise serializers.ValidationError({'current_password': 'You must provide the current password.'})

        if current_password and not password:
            raise serializers.ValidationError({'password': 'You must provide the new password.'})

        return data
