import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from yookassa import Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)

from cart.models import Order, Status
from cart.utils import get_client_ip


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
                    "orderNumber": f"{order.pk}",
                },
                "test": "test",
            },
        )

        return redirect(res.confirmation.confirmation_url)


class OrderUpdateView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        if not SecurityHelper().is_ip_trusted(ip):
            return HttpResponse(status=400)

        event_json = json.loads(request.body)
        try:
            notification_object = WebhookNotificationFactory().create(
                event_json,
            )
            response_object = notification_object.object

            if (
                notification_object.event
                == WebhookNotificationEventType.PAYMENT_SUCCEEDED
            ):
                order = Order.objects.get(
                    pk=response_object.metadata.get("orderNumber"),
                )
                status = Status.PAID

            elif (
                notification_object.event
                == WebhookNotificationEventType.PAYMENT_CANCELED
            ):
                order = Order.objects.get(
                    pk=response_object.metadata.get("orderNumber"),
                )
                status = Status.CANCELLED

            else:
                return HttpResponse(status=400)

            order.status = status
            order.save()

        except Exception:
            return HttpResponse(status=400)

        return HttpResponse(status=200)
