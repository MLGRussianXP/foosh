from django.contrib import admin

from cart.models import Order

__all__ = []


@admin.register(Order)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        Order.user.field.name,
        Order.school.field.name,
        Order.status.field.name,
    )
