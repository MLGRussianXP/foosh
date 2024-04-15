from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView

import catalog.models


__all__ = []


class ItemListView(LoginRequiredMixin, ListView):
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
    url = reverse_lazy(
        "catalog:category",
        kwargs={
            "category": catalog.models.Category.values[0],
        },
    )
