from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        verbose_name="Отображаемое имя пользователя"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email для входа",
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
        }
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Участник платформы"
        verbose_name_plural = "Участники платформы"
        ordering = ['email']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
