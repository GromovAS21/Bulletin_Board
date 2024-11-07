from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админка модели User
    """

    list_display = ("id", "email", "role", "is_staff", "is_active", "is_superuser")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email",)
