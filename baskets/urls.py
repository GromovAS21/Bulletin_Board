from django.urls import path

from baskets.apps import BasketsConfig
from baskets.views import BasketListAPIView, BasketRetrieveAPIView

app_name = BasketsConfig.name

urlpatterns = [
    path("baskets/", BasketListAPIView.as_view(), name="basket_list"),
    path("baskets/<int:pk>/", BasketRetrieveAPIView.as_view(), name="basket_retrieve")
]