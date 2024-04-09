from django.urls import path
from homepage import views


__all__ = []


app_name = "homepage"

urlpatterns = [
    path("", views.Home.as_view()),
]
