from django.db import models
from django.db.models import IntegerField

from announcements.models import Announcement
from baskets.models import Basket
from users.models import User


class Order(models.Model):
    """
    Модель заказа
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор заказа",
        related_name="orders",
        blank=True,
        null=True,

    )
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        verbose_name="Корзина заказа",
        blank=True,
        null=True,
    )
    goods = models.ManyToManyField(
        Announcement,
        verbose_name="Товары",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания заказа",
        auto_now_add=True,
    )
    amount = IntegerField(
        verbose_name="Сумма заказа",
        blank=True,
        null=True,
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии",
        blank=True,
        null=True
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        blank=True,
        null=True
    )
    CHOICES_STATUS = [
        ("unpaid", "Не оплачен"),
        ("paid", "Оплачен"),
        ]

    status = models.CharField(
        max_length=100,
        verbose_name="Статус заказа",
        choices=CHOICES_STATUS,
        default="unpaid"
    )


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-created_at",)

    def __str__(self):
        return f" Заказ № {self.pk}"
