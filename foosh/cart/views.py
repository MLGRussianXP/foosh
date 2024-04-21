from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from yookassa import Payment

from cart.models import Order


__all__ = []


class CheckoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")

    def get(self, request, *args, **kwargs):
        # add check if the cart is not empty
        # otherwise redirect to the cart page
        order = Order.objects.create(
            user=request.user.student,
            school=request.user.student.school,
        )

        # add items from the cart (now, every item from the current school)
        order.items.add(*request.user.student.school.items.all())
        # then, empty the cart

        total_price = sum(item.price for item in order.items.all())
        res = Payment.create(
            {
                "amount": {
                    "value": total_price,
                    "currency": "RUB",
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": settings.YOKASSA_SUCCESS_URL,
                },
                "capture": True,
                "description": f"Заказ №{order.pk}",
                "metadata": {
                    "orderNumber": "{order.pk}",
                },
                "test": "test",
            },
        )

        return redirect(res.confirmation.confirmation_url)
