from rest_framework import serializers

from django.contrib.auth import get_user_model

from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer
)

User = get_user_model()


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'user_role')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'message': 'Authenticated user data fetched successfully!',
            'user': data
        }


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    phone_number = serializers.CharField(required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'user_role')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'message': 'User registered successfully!',
            'user': data,
        }
