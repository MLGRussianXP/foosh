from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView

from users.forms import SchoolSignUpForm, StudentSignUpForm
from users.models import CustomUser


__all__ = []


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = "registration/student_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class SchoolSignUpView(CreateView):
    model = CustomUser
    form_class = SchoolSignUpForm
    template_name = "registration/school_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "school"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")
