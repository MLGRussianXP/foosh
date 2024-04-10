from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


__all__ = []


class CustomUser(AbstractUser):
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
    )

    name = models.CharField(
        "название",
        max_length=255,
        blank=False,
    )

    city = models.CharField(
        "город",
        max_length=255,
        blank=False,
    )

    def __str__(self):
        return f"{self.name} ({self.city})"


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
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

    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="школа",
    )
