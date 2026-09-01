from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Введите адрес почты",
    )
    tg_nick = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="TG name", help_text="Укажите телеграм ник"
    )
    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Телеграмм chat-id", help_text="Укажите телеграмм chat-id"
    )

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
