import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from cart.models import Cart, CartItem
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
