import pytest
from rest_framework.test import APIClient

from announcements.models import Review
from announcements.models import Announcement
from users.models import User

@pytest.fixture
def api_client():
    """
    Клиент для тестирования API
    """
    return APIClient()

@pytest.fixture
def user_is_owner_fixture():
    """
    фикстура модели User
    """
    user = User.objects.create(email="test@test.ru", password="Qwerty", is_active=True)
    return user

@pytest.fixture
def user_fixture():
    """
    фикстура модели User без авторизации
    """
    user = User.objects.create(email="test1@test.ru", password="Qwerty", is_active=True)
    return user

@pytest.fixture
def admin_fixture():
    """
    фикстура модели User без авторизации
    """
    user = User.objects.create(email="admin@test.ru", password="Qwerty", is_active=True, is_staff=True)
    return user

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