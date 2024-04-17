from django.contrib.auth import views
from django.urls import path

import users.forms
import users.views

app_name = "users"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=users.forms.CustomAuthForm,
        ),
        name="login",
    ),
    path(
        "signup/",
        users.views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "signup/student/",
        users.views.StudentSignUpView.as_view(),
        name="student_signup",
    ),
    path(
        "signup/school/",
        users.views.SchoolSignUpView.as_view(),
        name="school_signup",
    ),
    path(
        "load_schools/",
        users.views.LoadSchools.as_view(),
        name="load_schools",
    ),
]
