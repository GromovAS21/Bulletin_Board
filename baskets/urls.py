from django.urls import path

from baskets.apps import BasketsConfig
from baskets.views import BasketListAPIView, BasketRetrieveAPIView, BasksetAdditionOrDeleteAPIView

app_name = BasketsConfig.name

urlpatterns = [
    path("baskets/list/", BasketListAPIView.as_view(), name="basket_list"),
    path("baskets/<int:pk>/", BasketRetrieveAPIView.as_view(), name="basket_retrieve"),
    path("baskets/", BasksetAdditionOrDeleteAPIView.as_view(), name="basket_addition_or_delete")
]