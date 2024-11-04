from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели заказа
    """

    class Meta:
        model = Order
        exclude = ('session_id',)