from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from announcements.models import Announcement, Review
from announcements.serializers import AnnouncementAdminSerializer, AnnouncementSerializer, ReviewSerializer


class AnnouncementsListAPIView(generics.ListAPIView):
    """
    Выводит список всех объявлений
    """

    queryset = Announcement.objects.all()
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return AnnouncementAdminSerializer
        return AnnouncementSerializer


class AnnouncementsRetrieveAPIView(generics.RetrieveAPIView):
    """
    Выводит одно объявление по его id
    """

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return AnnouncementAdminSerializer
        return AnnouncementSerializer



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


class AnnouncementsDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляет объявление по его id
    """

    queryset = Announcement.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Review
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)