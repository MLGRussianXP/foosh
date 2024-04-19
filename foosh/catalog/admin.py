from catalog.models import Item
from django.contrib import admin

__all__ = []


@admin.register(Item)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        Item.name.field.name,
        Item.description.field.name,
        Item.image_tmb,
        Item.price.field.name,
        Item.category.field.name,
        Item.school.field.name,
    )
