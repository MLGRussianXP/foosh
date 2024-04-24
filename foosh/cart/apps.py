from django.apps import AppConfig


__all__ = []


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"
    verbose_name = "Корзина"
