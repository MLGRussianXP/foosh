from django.views.generic import TemplateView


__all__ = []


class Home(TemplateView):
    template_name = "homepage/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
