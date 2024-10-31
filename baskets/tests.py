import pytest
from django.urls import reverse
from rest_framework import status

from baskets.models import Basket

from announcements.tests.conftest import announcement_fixture
from users.tests.conftest import api_client, admin_fixture, user_is_owner_fixture, user_fixture


@pytest.fixture
def basket_fixture(user_is_owner_fixture):
    """
    Фикстура для создания корзины
    """

    return Basket.objects.create(author=user_is_owner_fixture)

@pytest.mark.django_db
def test_basket_list(api_client, basket_fixture, admin_fixture, user_is_owner_fixture):
    """
    Тестирование на вывод списка корзин
    """

    url = reverse("baskets:basket_list")
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 1

@pytest.mark.django_db
def test_basket_retrieve(api_client, user_fixture, user_is_owner_fixture, basket_fixture, admin_fixture):
    """
    Тестирование на вывод одной корзины
    """

    url = reverse("baskets:basket_retrieve", kwargs={"pk": basket_fixture.pk})
    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["goods"]) == 0

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["goods"]) == 0

@pytest.mark.django_db
def test_basket_addition_or_delete(api_client, user_is_owner_fixture, announcement_fixture, basket_fixture):
    """
    Тестирование добавления и удаления товара из корзины
    """

    url = reverse("baskets:basket_addition_or_delete")
    data = {
        "announcement_id": announcement_fixture.pk
    }
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.post(url, data)
    response_1 = api_client.post(url, data={})

    assert response_1.status_code == status.HTTP_400_BAD_REQUEST

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Товар добавлен в корзину"
    assert basket_fixture.goods.count() == 1

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Товар удален из корзины"
    assert basket_fixture.goods.count() == 0
    assert basket_fixture.amount == 0
