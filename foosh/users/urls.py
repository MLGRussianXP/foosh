from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path(
        "signup/",
        views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "signup/student/",
        views.StudentSignUpView.as_view(),
        name="student_signup",
    ),
    path(
        "signup/school/",
        views.SchoolSignUpView.as_view(),
        name="school_signup",
    ),
]
