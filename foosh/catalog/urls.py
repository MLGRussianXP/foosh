from catalog import converters, views

from django.urls import path, register_converter


register_converter(converters.CategoryConverter, "category")

app_name = "catalog"

urlpatterns = [
    path(
        "",
        views.NoCategoryRedirectView.as_view(),
        name="redirect",
    ),
    path(
        "<category:category>/",
        views.ItemListView.as_view(),
        name="category",
    ),
    path(
        "item/<int:pk>/",
        views.item,
        name="item",
    ),
]
