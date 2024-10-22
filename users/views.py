import secrets
from gc import get_objects

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Контроллер для модели User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()


    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.set_password(user.password)
        token = secrets.token_hex(16)
        user.token = token
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        user.save(update_fields=["token", "is_active", "password"])
        send_mail(
            "Активация учетной записи",
            f"Для активации учетной записи пройдите по ссылке {url}",
            EMAIL_HOST_USER,
            [user.email]
        )

class EmailConfirmAPIView(APIView):
    """
    Представление для подтверждения email-адреса пользователя
    """

    def get(self, request, token):

        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response({"message": "Ваша учетная запись подтверждена!"})


class ResetPasswordApiView(APIView):
    """
    Представление для сброса пароля
    """

    def post(self, request):

        email = request.data.get("email")
        if not email:
            return Response({"email": "Необходимо ввести email"})
        user = get_object_or_404(User, email=email)
        if user:
            host = self.request.get_host()
            url = f"http//:{host}/{user.pk}/{user.token}"
            send_mail(
                "Сброс пароля",
                f"Для восстановления пароля скопируйте нужные данные со ссылки: {url}",
                EMAIL_HOST_USER,
                [user.email]
            )
            return Response({"message":"На Вашу электронную почту направлено сообщение для изменения пароля"})


class ResetPasswordConfirmApiView(APIView):
    """
    Представление для cоздания пароля
    """

    def post(self, request):

       uid = request.data.get("uid")
       if not uid:
           return Response({"uid": "Необходимо ввести uid"})
       token = request.data.get("token")
       if not token:
           return Response({"token": "Необходимо ввести токен"})
       new_password = request.data.get("new_password")
       if not new_password:
           return Response({"new_password": "Необходимо ввести новый пароль"})
       elif len(new_password) < 8:
           return Response({"new_password": "Пароль должен быть не менее 8 символов"})
       user = get_object_or_404(User, pk=uid, token=token)
       if user:
           user.set_password(new_password)
           user.token = secrets.token_hex(16)
           user.save()
           return Response({"message":"Ваш пароль успешно изменен"})
