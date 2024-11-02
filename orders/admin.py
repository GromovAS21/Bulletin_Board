from IPython.core.release import author
from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    """
    Админка модели Order
    """

    list_display = ("id", "author", "amount", "status")
    list_filter = ("author", "status")
    search_fields = ("amount",)

