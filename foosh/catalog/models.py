from django.db import models
from django.utils.html import mark_safe
from sorl.thumbnail import get_thumbnail, ImageField

from users.models import School


__all__ = []


class Category(models.IntegerChoices):
    BAKERY = 1, "Выпечка"
    DRINKS = 2, "Напитки"
    HOT = 3, "Горячее"
    COMBO = 4, "Комбо"

    __empty__ = "..."


class Item(models.Model):
    name = models.CharField(
        "название",
        max_length=255,
        blank=False,
    )

    description = models.TextField(
        "описание",
        blank=False,
    )

    image = ImageField(
        "изображение",
        upload_to="catalog/",
    )

    price = models.DecimalField(
        "цена",
        max_digits=10,
        decimal_places=2,
        blank=False,
    )

    category = models.IntegerField(
        "категория",
        choices=Category.choices,
    )

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        verbose_name="школа",
        blank=False,
    )

    created_at = models.DateTimeField(
        "дата создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "дата ипзменения",
        auto_now=True,
    )

    def get_image_750x512(self):
        return get_thumbnail(
            self.image,
            "750x512",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" width="50">',
            )

        return "Нет изображения"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
