from django.db import models

from catalog.models import Item
from users.models import CustomUser, School, Student


__all__ = []


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="корзина",
    )


class CartItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="товар",
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cartitems",
        verbose_name="однотоварная корзина",
    )

    quantity = models.IntegerField(
        "количество",
        default=0,
    )

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"


class Status(models.IntegerChoices):
    CREATED = 1, "Создан"
    PAID = 2, "Оплачен"
    READY = 3, "Готов"
    CANCELLED = 4, "Отменен"


class Order(models.Model):
    user = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="orders",
    )

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        verbose_name="школа",
        related_name="orders",
    )

    total_price = models.DecimalField(
        "итого",
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )

    status = models.IntegerField(
        "статус",
        choices=Status.choices,
        default=Status.CREATED,
    )

    payment = models.CharField(
        "платеж",
        max_length=255,
    )

    created_at = models.DateTimeField(
        "создано",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "изменено",
        auto_now=True,
    )

    def __str__(self):
        return f"Заказ №{self.pk}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.total_price = sum(
                item.item.price * item.quantity for item in self.items.all()
            )

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="заказ",
        related_name="items",
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name="товар",
    )

    quantity = models.PositiveIntegerField(
        "количество",
        default=0,
    )

    class Meta:
        unique_together = ("order", "item")
