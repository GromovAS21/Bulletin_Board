from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from announcements.models import Announcement, Review
from announcements.paginations import ADSPagination, ListPagination
from announcements.serializers import (AnnouncementRetrieveAdminSerializer,
                                       AnnouncementRetrieveUserSerializer,
                                       AnnouncementSerializer,
                                       ReviewSerializer,
                                       ReviewUpdateSerializer)
from users.permissions import IsOwner


class AnnouncementsListAPIView(generics.ListAPIView):
    """
    Выводит список всех объявлений
    """

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = ListPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ("author",)
    search_fields = ("title",)
    ordering_fields = ("created_at",)


class AnnouncementListADSPaginator(AnnouncementsListAPIView):
    """
    Выводит список объявлений с пагинацией в 4 экземпляра
    """

    pagination_class = ADSPagination


class AnnouncementsRetrieveAPIView(generics.RetrieveAPIView):
    """
    Выводит одно объявление по его id
    """

    queryset = Announcement.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return AnnouncementRetrieveAdminSerializer
        return AnnouncementRetrieveUserSerializer


class AnnouncementsCreateAPIView(generics.CreateAPIView):
    """
    Создает новое объявление
    """

    serializer_class = AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnnouncementsUpdateAPIView(generics.UpdateAPIView):
    """
    Изменяет существующее объявление
    """

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)


class AnnouncementsDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляет объявление по его id
    """

    queryset = Announcement.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)


@method_decorator(name="list", decorator=swagger_auto_schema(operation_description="Представления всех отзывов"))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(operation_description="Представление одного отзыва"))
@method_decorator(name="create", decorator=swagger_auto_schema(operation_description="Представление создания отзыва"))
@method_decorator(name="update", decorator=swagger_auto_schema(operation_description="Представление изменения отзыва"))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(operation_description="Представление частичного изменения отзыва"))
@method_decorator(name="destroy", decorator=swagger_auto_schema(operation_description="Представление удаления отзыва"))
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Review
    """

    queryset = Review.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = ListPagination
    filterset_fields = ("author", "announcement")
    ordering_fields = ("created_at",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsOwner | IsAdminUser,)
        elif self.action == "retrieve":
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("update", "partial_update", "list", "retrieve"):
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Review.objects.all()
        try:
            return Review.objects.filter(author=self.request.user)
        except TypeError:
            return Review.objects.none()


class ReviewListADSPaginator(generics.ListAPIView):
    """
    Выводит список отзывов с пагинацией в 4 экземпляра
    """

    serializer_class = ReviewUpdateSerializer
    pagination_class = ADSPagination
    queryset = Review.objects.all()
    permission_classes = ()

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Review.objects.all()
        return Review.objects.filter(author=self.request.user)
