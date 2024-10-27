from django.contrib import admin

from baskets.models import Basket

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Админка модели Basket
    """

    list_display = ('id', "user")
    list_filter = ('user',)
