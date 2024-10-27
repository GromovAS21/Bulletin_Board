from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from announcements.paginations import ListPagination
from baskets.models import Basket
from baskets.serializers import BasketSerializer
from users.permissions import IsOwner


class BasketListAPIView(generics.ListAPIView):
    """
    Получение корзины пользователя
    """
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    pagination_class = ListPagination
    permission_classes = (IsAdminUser,)

class BasketRetrieveAPIView(generics.RetrieveAPIView):
    """
    Получение корзины пользователя
    """
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    permission_classes = (IsOwner| IsAdminUser, )





