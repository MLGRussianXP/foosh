from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView

import catalog.models

__all__ = []


class ItemListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("users:login")
    template_name = "catalog/catalog.html"
    context_object_name = "items"

    def get_queryset(self):
        user_school = self.request.user.student.school
        category = self.kwargs["category"]
        return catalog.models.Item.objects.filter(
            category=category,
            school=user_school,
        )


class NoCategoryRedirectView(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy("users:login")
    url = reverse_lazy(
        "catalog:category",
        kwargs={
            "category": catalog.models.Category.BAKERY,
        },
    )


def item(request, pk):
    template = "catalog/item.html"

    item = catalog.models.Item.objects.filter(id=pk).first()
    context = {
        "item": item,
        "title": item.name,
    }

    return render(request, template, context)
