from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from announcements.models import Announcement
from announcements.paginations import ListPagination
from baskets.models import Basket
from baskets.serializers import BasketSerializer, BasketAdditionSerializer
from users.permissions import IsOwner


class BasketListAPIView(generics.ListAPIView):
    """
    Получение всех корзин пользователей
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

class BasksetAdditionOrDeleteAPIView(APIView):
    """
    Добавление/Удаление товара в корзину
    """

    def post(self, request):
        serializer = BasketAdditionSerializer(data=request.data)
        announcement_id = request.data.get('announcement_id')

        if serializer.is_valid():
            basket = Basket.objects.get(author=request.user)
            announcement = get_object_or_404(Announcement, pk=announcement_id)

            if announcement:
                if announcement in basket.goods.all():
                    basket.goods.remove(announcement)
                    basket.amount -= announcement.price
                    basket.save(update_fields=["amount"])
                    return Response({"message": "Товар удален из корзины"})
                else:
                    basket.goods.add(announcement)
                    basket.amount += announcement.price
                    basket.save(update_fields=["amount"])
                    return Response({"message": "Товар добавлен в корзину"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
