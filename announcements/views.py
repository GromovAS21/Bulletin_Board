from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from announcements.models import Announcement, Review
from announcements.serializers import AnnouncementListSerializer, ReviewSerializer, AnnouncementRetrieveAdminSerializer, \
    AnnouncementRetrieveUserSerializer
from users.permissions import IsAdmin, IsOwner


class AnnouncementsListAPIView(generics.ListAPIView):
    """
    Выводит список всех объявлений
    """
    serializer_class = AnnouncementListSerializer
    queryset = Announcement.objects.all()
    permission_classes = (AllowAny, )



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
    permission_classes = (IsAdmin | IsOwner,)


class AnnouncementsDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляет объявление по его id
    """

    queryset = Announcement.objects.all()
    permission_classes = (IsAdmin | IsOwner,)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Review
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsOwner | IsAdmin,)
        elif self.action == "retrieve":
            self.permission_classes = (IsAdmin,)
        return super().get_permissions()

