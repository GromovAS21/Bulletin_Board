from django.urls import path
from rest_framework.routers import SimpleRouter

from announcements.apps import AnnouncementsConfig
from announcements.views import AnnouncementsListAPIView, AnnouncementsCreateAPIView, AnnouncementsRetrieveAPIView, \
    AnnouncementsUpdateAPIView, AnnouncementsDestroyAPIView, ReviewViewSet, AnnouncementListADSPaginator, \
    ReviewListADSPaginator

app_name = AnnouncementsConfig.name

router = SimpleRouter()
router.register(r"reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path('announcements/', AnnouncementsListAPIView.as_view(), name='announcements_list'),
    path('announcements/ads/', AnnouncementListADSPaginator.as_view(), name='announcements_list_ads'),
    path('announcements/<int:pk>/', AnnouncementsRetrieveAPIView.as_view(), name='announcements_retrieve'),
    path('announcements/create/', AnnouncementsCreateAPIView.as_view(), name='announcements_create'),
    path('announcements/<int:pk>/update/', AnnouncementsUpdateAPIView.as_view(), name='announcements_update'),
    path('announcements/<int:pk>/delete/', AnnouncementsDestroyAPIView.as_view(), name='announcements_delete'),

    path('reviews/ads/', ReviewListADSPaginator.as_view(), name='reviews_list_ads'),
    ] + router.urls