from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Проверяет, является ли пользователь суперпользователем
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsUserProfile(BasePermission):
    """
    Проверяет, является ли это профиль текущего пользователя
    """

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.email == obj.email
        except AttributeError:
            return False
