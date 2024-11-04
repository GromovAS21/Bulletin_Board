from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from baskets.models import Basket
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import create_stripe_product, create_price_stripe_product, create__stripe_session, \
    check_stripe_status_pay


class OrderAPIView(APIView):
    """
    Представление создание Заказа
    """

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        basket = Basket.objects.get(author=request.user)
        if basket.amount and serializer.is_valid():
            order = serializer.save()
            order.author = request.user
            order.basket = basket
            order.amount = basket.amount
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



