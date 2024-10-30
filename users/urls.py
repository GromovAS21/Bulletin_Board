from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, EmailConfirmAPIView, ResetPasswordApiView, ResetPasswordConfirmApiView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/email-confirm/<str:token>', EmailConfirmAPIView.as_view(permission_classes=(AllowAny,)), name='email_confirm'),
    path('users/reset_password/', ResetPasswordApiView.as_view(), name='reset_password'),
    path('users/reset_password_confirm/', ResetPasswordConfirmApiView.as_view(), name='reset_password'),
] + router.urls
