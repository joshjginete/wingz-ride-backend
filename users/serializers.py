from django.contrib.auth import get_user_model

from rest_framework import serializers

from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer
)

User = get_user_model()


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone_number',
            'user_role',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'user': data}


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    phone_number = serializers.CharField(required=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone_number',
            'user_role',
            'password',
            'confirm_password',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})

        if attrs.get('user_role') == User.ROLE_ADMIN and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError({
                "user_role": "Only superusers can assign admin role."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        if validated_data.get('user_role') == User.ROLE_ADMIN:
            validated_data['is_superuser'] = True
            validated_data['is_staff'] = True

        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'message': 'User registered successfully!',
            'user': data,
        }
