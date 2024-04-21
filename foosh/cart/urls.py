from django.urls import path

import cart.views


__all__ = []


app_name = "cart"

urlpatterns = [
    path("cart/", cart.views.CartView.as_view(), name="cart_view"),
    path(
        "update_item_in_cart/",
        cart.views.UpdateItemInCart.as_view(),
        name="update_item_in_cart",
    ),
]
