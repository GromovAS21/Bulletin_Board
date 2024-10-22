from rest_framework import serializers

from announcements.models import Announcement, Review


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Announcement
    """

    class Meta:
        model = Announcement
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review
    """

    class Meta:
        model = Review
        fields = "__all__"