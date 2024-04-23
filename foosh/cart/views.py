import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from yookassa import Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)

from cart.models import Cart, CartItem, Order, Status
from cart.utils import get_client_ip
from catalog.models import Item


__all__ = []


class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("users:login")

        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
        )
        context["cartitems"] = CartItem.objects.filter(cart=cart)
        context["title"] = "FOOSH"

        return context


class UpdateItemInCart(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")

        data = json.loads(self.request.body)
        product_id = data["product_id"]
        action = data["action"]

        item = Item.objects.get(id=product_id)
        cart, cart_created = Cart.objects.get_or_create(
            user=request.user,
        )
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            cart=cart,
            item=item,
        )

        if action == "add":
            cart_item.quantity += 1
        elif action == "remove":
            cart_item.quantity -= 1

        cart_item.save()

        if cart_item.quantity <= 0:
            cart_item.delete()

        return JsonResponse("Item was added", safe=False)


class CheckoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")

    def get(self, request, *args, **kwargs):
        # add check if the cart is not empty
        # otherwise redirect to the cart page
        order = Order.objects.create(
            user=request.user.student,
            school=request.user.student.school,
        )
        order.save()

        # add items from the cart (now, every item from the current school)
        order.items.add(*request.user.student.school.items.all())
        order.save()
        # then, empty the cart

        res = Payment.create(
            {
                "amount": {
                    "value": order.total_price,
                    "currency": "RUB",
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": settings.YOKASSA_SUCCESS_URL,
                },
                "capture": True,
                "description": f"Заказ №{order.pk}",
                "metadata": {
                    "orderNumber": order.pk,
                },
                "test": "test",
            },
        )

        payment_url = res.confirmation.confirmation_url
        order.payment = payment_url
        order.save()

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
