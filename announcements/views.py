from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import AllowAny, IsAdminUser

from announcements.models import Announcement, Review
from announcements.serializers import AnnouncementListSerializer, ReviewSerializer, AnnouncementRetrieveAdminSerializer, \
    AnnouncementRetrieveUserSerializer
from users.permissions import IsOwner


class AnnouncementsListAPIView(generics.ListAPIView):
    """
    Выводит список всех объявлений
    """
    serializer_class = AnnouncementListSerializer
    queryset = Announcement.objects.all()
    permission_classes = (AllowAny, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ("author",)
    search_fields = ("title",)
    ordering_fields = ("created_at",)



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

    serializer_class = AnnouncementListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnnouncementsUpdateAPIView(generics.UpdateAPIView):
    """
    Изменяет существующее объявление
    """

    serializer_class = AnnouncementListSerializer
    queryset = Announcement.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)


class AnnouncementsDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляет объявление по его id
    """

    queryset = Announcement.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Review
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
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

