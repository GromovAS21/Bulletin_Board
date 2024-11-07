from django.urls import path

from orders.apps import OrdersConfig
from orders.views import (OrderAPIView, OrderDeleteAPIView, OrderListView,
                          OrderRetrieveAPIView, OrderUpdateAPIView,
                          success_pay)

app_name = OrdersConfig.name

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderRetrieveAPIView.as_view(), name="orders_retrieve"),
    path("orders/create/", OrderAPIView.as_view(), name="orders_create"),
    path("orders/<int:pk>/update/", OrderUpdateAPIView.as_view(), name="orders_update"),
    path("orders/<int:pk>/delete/", OrderDeleteAPIView.as_view(), name="orders_delete"),
    path("orders/success_pay/", success_pay, name="orders_success_pay"),
]
