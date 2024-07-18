from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="укажите почту"
    )
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="телефон")
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="аватар", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
