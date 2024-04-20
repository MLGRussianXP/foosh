from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from cart.models import Order, Status


__all__ = []


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # add check if the cart is not empty
        # otherwise redirect to the card page
        order = Order.objects.create(
            user=request.user.student,
            school=request.user.student.school,
        )

        # add items from the cart (now, every item from the current school)
        order.items.add(*request.user.student.school.items.all())
        # then, empty the cart

        # integrate the payments...
        order.status = Status.PAID

        # redirect to the orders page
        return redirect("/")
