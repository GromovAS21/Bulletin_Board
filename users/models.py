from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя
    """

    username = None

    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11)],
        verbose_name="Телефон",
        blank = True,
        null = True
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("user", "Пользователь"),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )
    image = models.ImageField(
        upload_to="users/",
        verbose_name="Аватар пользователя",
        blank=True,
        null=True
    )
    token = models.CharField(
        max_length=50,
        editable=False,
        verbose_name="Токен пользователя",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.email
