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
        "logout/",
        views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=users.forms.CustomPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=users.forms.CustomPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
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
