from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс для модели Пользователь"""

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите email"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
