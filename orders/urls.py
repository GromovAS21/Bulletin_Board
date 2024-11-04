from django.urls import path

from orders.apps import OrdersConfig
from orders.views import OrderAPIView, success_pay, OrderListView, OrderRetrieveAPIView, OrderUpdateAPIView, \
    OrderDeleteAPIView

app_name = OrdersConfig.name

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderRetrieveAPIView.as_view(), name="order_retrieve"),
    path("orders/create/", OrderAPIView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", OrderUpdateAPIView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteAPIView.as_view(), name="order_delete"),
    path("orders/success_pay/", success_pay, name="order_success_pay"),
]