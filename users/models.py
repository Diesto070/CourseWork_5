from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=False)

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    tg_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Телеграмм chat-id",
        help_text="Укажите телеграмм chat-id",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
