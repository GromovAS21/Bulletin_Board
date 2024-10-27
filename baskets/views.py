from rest_framework import generics

from baskets.models import Basket
from baskets.serializers import BasketSerializer


class BasketListAPIView(generics.ListAPIView):
    """
    Получение корзины пользователя
    """
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()