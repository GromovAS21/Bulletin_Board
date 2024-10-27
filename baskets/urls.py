from tkinter.font import names

from django.urls import path

from baskets.apps import BasketsConfig
from baskets.views import BasketListAPIView

app_name = BasketsConfig.name

urlpatterns = [
    path("baskets/", BasketListAPIView.as_view(), name="basket_list")
]