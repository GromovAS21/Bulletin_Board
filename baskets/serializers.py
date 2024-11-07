from rest_framework import serializers

from baskets.models import Basket


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Basket
    """

    class Meta:
        model = Basket
        fields = "__all__"


class BasketAdditionSerializer(serializers.Serializer):
    """
    Сериализатор для добавления товара в корзину
    """

    announcement_id = serializers.IntegerField(required=True)
