from rest_framework import serializers

from announcements.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Announcement
    """

    class Meta:
        model = Announcement
        fields = "__all__"
