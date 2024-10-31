from rest_framework import serializers

from users.models import User

class ProfileCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания профиля пользователя
    """

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "phone", "image")


class ProfileUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User (для пользователей)
    """

    email = serializers.EmailField(read_only=True)

    class Meta:

        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "image")


class ProfileAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User (для администратора)
    """

    class Meta:

        model = User
        fields = "__all__"


class ResetPasswordSerializer(serializers.Serializer):
    """
    Сериализатор для смены пароля
    """

    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Сериализатор для смены пароля
    """

    uid = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=8, required=True)



