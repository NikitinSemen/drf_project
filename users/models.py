from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

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

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("by_transfer", "По карте"),
        ("by_cash", "Наличными"),
    ]
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, **NULLABLE
    )
    date_of_payment = models.DateTimeField(auto_now_add=True)
    paid_lesson = models.ForeignKey(
        Lesson, verbose_name="Урок", on_delete=models.SET_NULL, **NULLABLE
    )
    paid_course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.SET_NULL, **NULLABLE
    )
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="by_transfer"
    )
    amount = models.PositiveIntegerField(verbose_name="сумма платежа", help_text='укажите сумму платежа', default=0)
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)
    session_id = models.CharField(max_length=255, verbose_name='ID сессии', **NULLABLE)

    def __str__(self):
        return f"{self.date_of_payment} - {self.amount}"


class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользватель", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Поодписки"
