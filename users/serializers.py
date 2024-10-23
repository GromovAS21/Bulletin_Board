from rest_framework import serializers

from users.models import User


class ProfileUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User (для пользователей)
    """

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:

        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "image", "password")


class ProfileAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User (для администратора)
    """

    class Meta:

        model = User
        fields = "__all__"