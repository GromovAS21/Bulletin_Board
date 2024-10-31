import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User


@pytest.mark.django_db
def test_user_create(client):
    """
    Тестирование создания нового пользователя
    """

    url = reverse("users:users-list")
    data = {
        "email": "test_new@test.ru",
        "password": "Qwerty123"
    }
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

@pytest.mark.django_db
def tests_user_list(api_client, user_fixture, admin_fixture):
    """
    Тестирование просмотра списка пользователей
    """

    url = reverse("users:users-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 2

@pytest.mark.django_db
def test_user_retrieve(api_client, user_fixture, user_is_owner_fixture, admin_fixture):
    """
    Тестирование просмотра одного пользователя
    """

    url = reverse("users:users-detail", kwargs={"pk": user_is_owner_fixture.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "test@test.ru"

@pytest.mark.django_db
def test_user_update(api_client, user_fixture, user_is_owner_fixture, admin_fixture):
    """
    Тестирование изменения информации о пользователе
    """

    url = reverse("users:users-detail", kwargs={"pk": user_is_owner_fixture.pk})
    data = {
        "first_name": "Test"
    }
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Test"

@pytest.mark.django_db
def test_user_delete(api_client, user_fixture, user_is_owner_fixture):
    """
    Тестирование удаления пользователя
    """

    url = reverse("users:users-detail", kwargs={"pk": user_is_owner_fixture.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 1
