from cities_light.models import City
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, View

from cart.models import Order
import users.forms
from users.models import CustomUser, School, Student


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
        kwargs["title"] = "Регистрация"

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
        kwargs["title"] = "Регистрация"

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
    def get(self, request, nav, *args, **kwargs):
        if request.user.is_student:
            template_name = "users/student_profile.html"

            user = Student.objects.filter(user_id=request.user.id).first()
            user_orders = Order.objects.filter(user=user).order_by(
                "-created_at",
            )

            context = {
                "orders": user_orders,
                "title": "Личный кабинет",
            }

            return render(request, template_name, context)

        if request.user.is_school:
            if nav == "orders":
                template_name = "users/school_profile_orders.html"

                school = School.objects.filter(user_id=request.user.id).first()
                user_orders = Order.objects.filter(school=school).order_by(
                    "-created_at",
                )

                context = {
                    "orders": user_orders,
                    "title": "Список заказов",
                }

                return render(request, template_name, context)

            if nav == "menu":
                template_name = "users/school_profile_menu.html"

                context = {
                    "title": "Список товаров",
                }

                return render(request, template_name, context)

        return redirect("users:signup")
