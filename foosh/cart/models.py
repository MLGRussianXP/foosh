from django.db import models

from catalog.models import Item
from users.models import CustomUser


__all__ = ()


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
        default=0,
        verbose_name="количество",
    )

    def __str__(self):
        return self.product.name.field.name
