from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Каталог"

        return context


class NoCategoryRedirectView(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy("users:login")
    url = reverse_lazy(
        "catalog:category",
        kwargs={
            "category": catalog.models.Category.BAKERY,
        },
    )


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"

    def get_object(self):
        pk = self.kwargs["pk"]
        return catalog.models.Item.objects.filter(id=pk).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Каталог"

        return context
