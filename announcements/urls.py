from django.urls import path
from rest_framework.routers import DefaultRouter

from announcements.apps import AnnouncementsConfig
from announcements.views import AnnouncementsListAPIView, AnnouncementsCreateAPIView, AnnouncementsRetrieveAPIView, \
    AnnouncementsUpdateAPIView, AnnouncementsDestroyAPIView, ReviewViewSet, AnnouncementListADSPaginator

app_name = AnnouncementsConfig.name

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path('announcements/', AnnouncementsListAPIView.as_view(), name='announcements_list'),
    path('announcements/ads/', AnnouncementListADSPaginator.as_view(), name='announcements_list_ads'),
    path('announcements/<int:pk>/', AnnouncementsRetrieveAPIView.as_view(), name='announcements_retrieve'),
    path('announcements/create/', AnnouncementsCreateAPIView.as_view(), name='announcements_create'),
    path('announcements/<int:pk>/update/', AnnouncementsUpdateAPIView.as_view(), name='announcements_update'),
    path('announcements/<int:pk>/delete/', AnnouncementsDestroyAPIView.as_view(), name='announcements_delete'),
] + router.urls