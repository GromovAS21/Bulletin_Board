from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    class Meta:

        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "image", "is_active", "is_staff", "is_superuser")
        read_only_fields = ("is_active", "is_staff", "is_superuser")


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового пользователя
    """

    class Meta:

        model = User
        fields = ("email", "password")
