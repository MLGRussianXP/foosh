from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


__all__ = []


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
    )

    is_student = models.BooleanField(
        "ученик",
        default=False,
    )

    is_school = models.BooleanField(
        "школа",
        default=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class School(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="пользователь",
    )

    name = models.CharField(
        "название",
        max_length=255,
        blank=False,
    )

    city = models.ForeignKey(
        "cities_light.City",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="город",
    )

    class Meta:
        verbose_name = "школа"
        verbose_name_plural = "школы"

    def __str__(self):
        return f"{self.name} ({self.city})"


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="пользователь",
    )

    name = models.CharField(
        "имя",
        max_length=100,
        blank=False,
    )

    surname = models.CharField(
        "фамилия",
        max_length=100,
        blank=False,
    )

    patronymic = models.CharField(
        "отчество",
        max_length=100,
    )

    city = models.ForeignKey(
        "cities_light.City",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="город",
    )

    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="школа",
    )

    def __str__(self):
        return f"{self.name} {self.surname} {self.patronymic}"

    class Meta:
        verbose_name = "ученик"
        verbose_name_plural = "ученики"
