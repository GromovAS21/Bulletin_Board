from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from announcements.paginations import ListPagination
from baskets.models import Basket
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import (check_stripe_status_pay, create__stripe_session,
                             create_price_stripe_product,
                             create_stripe_product)
from users.permissions import IsOwner


class OrderListView(generics.ListAPIView):
    """
    Представление получение списка Заказов
    """

    serializer_class = OrderSerializer
    pagination_class = ListPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(author=self.request.user)


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление получение Заказа
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsOwner | IsAdminUser,)


class OrderUpdateAPIView(generics.UpdateAPIView):
    """
    Представление изменения Заказа
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAdminUser,)


class OrderDeleteAPIView(generics.DestroyAPIView):
    """
    Представление удаления Заказа
    """

    queryset = Order.objects.all()
    permission_classes = (IsAdminUser,)


class OrderAPIView(APIView):
    """
    Представление создание Заказа
    """

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        basket = Basket.objects.get(author=request.user)
        basket_goods = basket.goods.all()
        if basket.amount and serializer.is_valid():
            order = serializer.save()
            order.author = request.user
            order.basket = basket
            order.amount = basket.amount
            order.goods.set(basket_goods)
            stripe_prod = create_stripe_product(order)
            stripe_price = create_price_stripe_product(order, stripe_prod)
            session_id, url = create__stripe_session(stripe_price)
            order.session_id = session_id
            order.link = url
            order.status = check_stripe_status_pay(session_id)
            order.save()
            basket.goods.clear()
            basket.amount = 0
            basket.save()
            return Response(serializer.data)
        else:
            return Response({"message": "Корзина пуста"}, status=400)


def success_pay(request):
    """
    Страница с успешной оплатой
    """

    orders = Order.objects.filter(status="unpaid")
    if orders:
        for order in orders:
            order.status = check_stripe_status_pay(order.session_id)
            order.save(update_fields=["status"])

    return render(request, "orders/success_pay.html")
