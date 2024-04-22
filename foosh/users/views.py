from cities_light.models import City
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, DecimalField, Prefetch, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, View

from cart.models import Order
from catalog.models import Item
import users.forms
from users.models import CustomUser, School


__all__ = []


class SignUpView(TemplateView):
    template_name = "users/signup.html"


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = users.forms.StudentSignUpForm
    template_name = "users/student_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        kwargs["cities"] = City.objects.all()
        kwargs["schools"] = School.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class SchoolSignUpView(CreateView):
    model = CustomUser
    form_class = users.forms.SchoolSignUpForm
    template_name = "users/school_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "school"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class LoadSchools(TemplateView):
    template_name = "users/school_options.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_id = self.request.GET.get("city")
        schools = School.objects.filter(city_id=city_id)
        context["schools"] = schools
        return context


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            template_name = "users/school_profile_orders.html"
        elif request.user.is_school:
            template_name = "users/school_profile_orders.html"

            orders = (
                Order.objects.filter(school_id=request.user.id)
                .annotate(
                    total_items=Count("items"),
                    total_price=Coalesce(
                        Sum("items__price"),
                        0,
                        output_field=DecimalField(),
                    ),
                )
                .prefetch_related(
                    Prefetch(
                        "items",
                        queryset=Item.objects.select_related("school"),
                    ),
                )
            )

            user_name = (
                School.objects.filter(user_id=request.user.id)
                .values("name")
                .first()
            )

            context = {
                "orders": orders,
                "user_email": request.user.email,
                "user_name": user_name,
            }

            return render(request, template_name, context)

        else:
            return redirect("users:signup")
