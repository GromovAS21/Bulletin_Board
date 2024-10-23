from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from announcements.models import Announcement, Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review
    """

    author = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class AnnouncementListSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Announcement для просмотра всех объявлений
    """
    author = serializers.CharField(read_only=True)
    reviews = SerializerMethodField(read_only=True)


    class Meta:
        model = Announcement
        exclude = ("created_at",)

    def get_reviews(self, obj):
        return Review.objects.filter(announcement=obj).count()


class AnnouncementRetrieveUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Announcement для просмотра конкретного объявления (для пользователя)
    """

    author = serializers.CharField(read_only=True)
    reviews = ReviewSerializer(source="announcement_reviews", many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = ("id", "title", "price", "description", "author", "reviews")


class AnnouncementRetrieveAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Announcement для просмотра конкретного объявления (для админа)
    """

    author = serializers.CharField(read_only=True)
    reviews = ReviewSerializer(source="announcement_reviews", many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = ("id", "title", "price", "description", "author", "created_at", "reviews")
