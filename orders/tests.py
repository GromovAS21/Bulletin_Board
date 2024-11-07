import pytest
from django.urls import reverse
from rest_framework import status

from announcements.tests.conftest import announcement_fixture
from baskets.tests import basket_fixture
from orders.models import Order
from users.tests.conftest import (admin_fixture, api_client, user_fixture,
                                  user_is_owner_fixture)


@pytest.fixture
def order_fixture(user_is_owner_fixture, basket_fixture, announcement_fixture):
    """
    Фикстура для создания заказа
    """

    order = Order.objects.create(author=user_is_owner_fixture, basket=basket_fixture)
    order.goods.add(announcement_fixture)
    return order


@pytest.mark.django_db
def test_order_list(api_client, order_fixture, user_is_owner_fixture, user_fixture):
    """
    Тестирование получения списка заказов
    """

    url = reverse("orders:orders_list")
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 1

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 0


@pytest.mark.django_db
def test_order_retrieve(api_client, order_fixture, user_is_owner_fixture, user_fixture):
    """
    Тестирование получения одного заказа
    """

    url = reverse("orders:orders_retrieve", kwargs={"pk": order_fixture.pk})
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["author"] == user_is_owner_fixture.pk

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_order_update(api_client, order_fixture, user_is_owner_fixture, admin_fixture):
    """
    Тест изменения заказа
    """

    url = reverse("orders:orders_update", kwargs={"pk": order_fixture.pk})
    data = {
        "status": "paid",
    }
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "paid"


@pytest.mark.django_db
def test_order_delete(api_client, order_fixture, user_is_owner_fixture, admin_fixture):
    """
    Тест удаления заказа
    """

    url = reverse("orders:orders_delete", kwargs={"pk": order_fixture.pk})
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_order_create(api_client, order_fixture, user_is_owner_fixture, basket_fixture, announcement_fixture):
    """
    Тест создания заказа
    """

    url = reverse("orders:orders_create")
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Корзина пуста"
