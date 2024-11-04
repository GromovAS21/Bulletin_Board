from django.urls import path

from orders.apps import OrdersConfig
from orders.views import OrderAPIView, success_pay

app_name = OrdersConfig.name

urlpatterns = [
    path("orders/create/", OrderAPIView.as_view(), name="order_create"),
    path("orders/success_pay/", success_pay, name="order_success_pay"),
]