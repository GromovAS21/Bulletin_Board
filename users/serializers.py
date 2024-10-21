from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    class Meta:

        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "image")


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    class Meta:

        model = User
        fields = ("email", "password")