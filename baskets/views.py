from django.shortcuts import render
from rest_framework import generics

from baskets.models import Basket
from baskets.serializers import BasketSerializer


class BasketListAPIView(generics.ListAPIView):
    """
    Получение списка товаров в корзине
    """
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()