from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админка модели Order
    """

    list_display = ("id", "author", "amount", "status")
    list_filter = ("author", "status")
    search_fields = ("amount",)

