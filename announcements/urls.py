from django.urls import path

from announcements.apps import AnnouncementsConfig
from announcements.views import AnnouncementsListAPIView, AnnouncementsCreateAPIView, AnnouncementsRetrieveAPIView, \
    AnnouncementsUpdateAPIView, AnnouncementsDestroyAPIView

app_name = AnnouncementsConfig.name

urlpatterns = [
    path('announcements/', AnnouncementsListAPIView.as_view(), name='announcements_list'),
    path('announcements/<int:pk>', AnnouncementsRetrieveAPIView.as_view(), name='announcements_retrieve'),
    path('announcements/create/', AnnouncementsCreateAPIView.as_view(), name='announcements_create'),
    path('announcements/<int:pk>/update/', AnnouncementsUpdateAPIView.as_view(), name='announcements_update'),
    path('announcements/<int:pk>/delete/', AnnouncementsDestroyAPIView.as_view(), name='announcements_delete'),
]