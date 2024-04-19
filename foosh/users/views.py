from cities_light.models import City

from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView

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
