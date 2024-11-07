import pytest
from django.urls import reverse
from rest_framework import status

from announcements.models import Review
from users.tests.conftest import (admin_fixture, api_client, user_fixture,
                                  user_is_owner_fixture)


@pytest.mark.django_db
def test_review_create(api_client, user_fixture, announcement_fixture):
    """
    Тест создания нового отзыва
    """

    url = reverse("announcements:reviews-list")
    data = {"text": "new text", "announcement": announcement_fixture.pk}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == data["text"]
    assert Review.objects.count() == 1
    assert Review.objects.first().author == user_fixture


@pytest.mark.django_db
def test_review_list(api_client, review_fixture, user_is_owner_fixture, user_fixture):
    """
    Тест получения списка отзывов
    """
    url = reverse("announcements:reviews-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 0

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 1


@pytest.mark.django_db
def test_review_retrieve(api_client, review_fixture, user_is_owner_fixture, admin_fixture):
    """
    Тест получения одного отзыва
    """

    url = reverse("announcements:reviews-detail", kwargs={"pk": review_fixture.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "test text"


@pytest.mark.django_db
def test_review_update(api_client, review_fixture, user_is_owner_fixture, user_fixture):
    """
    Тест изменения отзыва
    """

    url = reverse("announcements:reviews-detail", kwargs={"pk": review_fixture.pk})
    data = {
        "text": "test text updated",
    }

    response = api_client.patch(url, data)
    response_1 = api_client.put(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_1.status_code == status.HTTP_404_NOT_FOUND

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.patch(url, data)
    response_1 = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response_1.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "test text updated"

    api_client.force_authenticate(user_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_review_delete(api_client, review_fixture, user_is_owner_fixture, user_fixture):
    """
    Тест удаления отзыва
    """

    url = reverse("announcements:reviews-detail", kwargs={"pk": review_fixture.pk})

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
