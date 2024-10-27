from django.db import models

from announcements.models import Announcement
from users.models import User


class Basket(models.Model):
    """
    Модель корзины
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True
    )
    goods = models.ManyToManyField(
        Announcement,
        verbose_name="Товары",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма к оплате",
        default=0
    )

    class Meta:
        verbose_name = "Корзина",
        verbose_name_plural = "Корзины",
        ordering = ("id",)

    def __str__(self):
        return f"Корзина {self.user.email}"