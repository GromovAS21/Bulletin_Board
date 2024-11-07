from django.contrib import admin

from announcements.models import Announcement, Review


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Админка модели Announcement
    """

    list_display = ("id", "title", "price", "author", "created_at")
    list_filter = ("author",)
    search_fields = ("title", "price")


@admin.register(Review)
class Review(admin.ModelAdmin):
    """
    Админка модели Review
    """

    list_display = ("id", "text", "author", "announcement", "created_at")
    list_filter = ("author", "announcement")
    search_fields = ("text",)
