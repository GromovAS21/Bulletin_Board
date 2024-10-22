from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:

        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "image", "password")