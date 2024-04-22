from django.urls import path
from django.views.decorators.csrf import csrf_exempt

import cart.views

__all__ = []


app_name = "cart"

urlpatterns = [
    path(
        "checkout/",
        cart.views.CheckoutView.as_view(),
        name="checkout",
    ),
    path(
        "order_update/",
        csrf_exempt(cart.views.OrderUpdateView.as_view()),
        name="order_update",
    ),
]
