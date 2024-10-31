import pytest
from django.urls import reverse
from pytest_django.fixtures import client
from rest_framework import status
from users.tests.conftest import user_fixture, user_is_owner_fixture, api_client

from announcements.models import Announcement


@pytest.mark.django_db
def test_announcement_list(announcement_fixture, client):
    """
    Тестирование просмотра списка объявлений
    """

    url = reverse("announcements:announcements_list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["results"][0]["title"] == "test title"


@pytest.mark.django_db
def test_announcement_retrieve(api_client, user_is_owner_fixture, user_fixture, announcement_fixture):
    """
    Тестирование просмотра одного объявления
    """
    url = reverse("announcements:announcements_retrieve", kwargs={"pk": announcement_fixture.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user=user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "test title"

@pytest.mark.django_db

def test_announcement_update(api_client, user_is_owner_fixture, user_fixture, announcement_fixture):
    """
    Тестирование изменения информации об объявлении
    """

    url = reverse("announcements:announcements_update", kwargs={"pk": announcement_fixture.pk})
    data = {
        "title": "test_title_updated",
        "price": 200,
    }
    response = api_client.put(url, data)
    response_1 = api_client.patch(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_1.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)
    response_1 = api_client.patch(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response_1.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.put(url, data)
    response_1 = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response_1.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "test_title_updated"

@pytest.mark.django_db
def test_announcement_delete(api_client, user_is_owner_fixture, user_fixture, announcement_fixture):
    """
    Тестирование удаления объявления
    """

    url = reverse("announcements:announcements_delete", kwargs={"pk": announcement_fixture.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Announcement.objects.count() == 0
