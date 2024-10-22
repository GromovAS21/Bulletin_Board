from django.db import models

from users.models import User


class Announcement(models.Model):
    """
    Модель объявления
    """

    title = models.CharField(
        max_length=50,
        verbose_name="Название товара",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена товара",
    )
    description = models.TextField(
        verbose_name="Описание товара",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор объявления",
        blank=True,
        null=True,
        related_name="announcements",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Модель отзыва
    """

    text = models.TextField(
        verbose_name="Текст отзыва",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Автор отзыва",
        blank=True,
        null=True,
        related_name="author_reviews",
    )
    ad = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        verbose_name="Объявление",
        related_name="announcement_reviews",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.author}"

