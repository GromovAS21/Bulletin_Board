from rest_framework import serializers

from announcements.models import Announcement, Review


class AnnouncementAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Announcement для администраторов
    """

    class Meta:
        model = Announcement
        fields = "__all__"

class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Announcement для пользователей
    """

    class Meta:
        model = Announcement
        exclude = ("author", "created_at")


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review
    """

    class Meta:
        model = Review
        fields = "__all__"