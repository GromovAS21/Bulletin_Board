from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from announcements.models import Announcement
from announcements.serializers import AnnouncementSerializer


class AnnouncementsListAPIView(generics.ListAPIView):
    """
    Выводит список всех объявлений
    """

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = (AllowAny, )


class AnnouncementsRetrieveAPIView(generics.RetrieveAPIView):
    """
    Выводит одно объявление по его id
    """

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()


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