import secrets

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from announcements.paginations import ListPagination
from announcements.tasks import send_mail_from_email
from baskets.models import Basket
from config.settings import EMAIL_HOST_USER
from users.models import User
from users.permissions import IsSuperUser, IsUserProfile
from users.serializers import (ProfileAdminSerializer, ProfileCreateSerializer,
                               ProfileUserSerializer,
                               ResetPasswordConfirmSerializer,
                               ResetPasswordSerializer)


@method_decorator(name="list", decorator=swagger_auto_schema(operation_description="Представление списка всех пользователей"))
@method_decorator(name="create", decorator=swagger_auto_schema(operation_description="Представление создания пользователя"))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(operation_description="Представление просмотра конкретного пользователя"))
@method_decorator(name="update", decorator=swagger_auto_schema(operation_description="Представление изменения пользователя"))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(operation_description="Представление частичного изменения пользователя"))
@method_decorator(name="destroy", decorator=swagger_auto_schema(operation_description="Представление удаления пользователя"))
class UserViewSet(viewsets.ModelViewSet):
    """
    Контроллер для модели User
    """

    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    pagination_class = ListPagination
    search_fields = ("email",)
    filterset_fields = ("role", "is_active", "is_staff")

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ProfileAdminSerializer
        if self.action == "create":
            return ProfileCreateSerializer
        return ProfileUserSerializer

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = (IsAdminUser,)
        if self.action in ("update", "partial_update"):
            self.permission_classes = (IsAdminUser | IsUserProfile,)
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        if self.action == "retrieve":
            self.permission_classes = (IsUserProfile | IsAdminUser,)
        if self.action == "destroy":
            self.permission_classes = (IsSuperUser | IsUserProfile,)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.set_password(user.password)
        Basket.objects.create(author=user)
        token = secrets.token_hex(16)
        user.token = token
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        user.save(update_fields=["token", "is_active", "password"])
        send_mail_from_email.delay(
            "Активация учетной записи",
            f"Для активации учетной записи пройдите по ссылке {url}",
            EMAIL_HOST_USER,
            [user.email],
        )


class EmailConfirmAPIView(APIView):
    """
    Представление для подтверждения email-адреса пользователя
    """

    @swagger_auto_schema(responses={200: "Ваша учетная запись подтверждена!"})
    def get(self, request, token):

        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response({"message": "Ваша учетная запись подтверждена!"})


class ResetPasswordApiView(APIView):
    """
    Представление для сброса пароля
    """

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={
            200: "На Вашу электронную почту направлено сообщение для изменения пароля",
            400: "BAD_REQUEST",
        },
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get("email")
            user = get_object_or_404(User, email=email)
            if user:
                send_mail_from_email.delay(
                    subject="Сброс пароля",
                    message=f"Данные для восстановления пароля:"
                    f"\nuid: {user.pk}"
                    f"\ntoken: {user.token}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return Response(
                    {
                        "message": "На Вашу электронную почту направлено сообщение для изменения пароля"
                    }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmApiView(APIView):
    """
    Представление для cоздания пароля
    """

    @swagger_auto_schema(
        request_body=ResetPasswordConfirmSerializer,
        responses={200: "Ваш пароль успешно изменен", 400: "BAD_REQUEST"},
    )
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = request.data.get("uid")
            token = request.data.get("token")
            new_password = request.data.get("new_password")
            user = get_object_or_404(User, pk=uid, token=token)
            if user:
                user.set_password(new_password)
                user.token = secrets.token_hex(16)
                user.save()
                return Response({"message": "Ваш пароль успешно изменен"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
