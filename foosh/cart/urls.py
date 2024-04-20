from django.urls import path

import cart.views

__all__ = []


app_name = "cart"

urlpatterns = [
    path("checkout/", cart.views.CheckoutView.as_view(), name="checkout"),
]
