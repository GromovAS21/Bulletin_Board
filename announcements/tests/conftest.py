import pytest

from announcements.models import Review
from announcements.models import Announcement


@pytest.fixture
def announcement_fixture(user_is_owner_fixture):
    """
    фикстура модели Announcement
    """
    announcement = Announcement.objects.create(title="test title", price=100, author=user_is_owner_fixture)
    return announcement

@pytest.fixture
def review_fixture(user_is_owner_fixture, announcement_fixture):
    """
    фикстура модели Review
    """

    return Review.objects.create(text="test text", author=user_is_owner_fixture, announcement=announcement_fixture)