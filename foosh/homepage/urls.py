from django.urls import path

import homepage.views

__all__ = []


app_name = "homepage"

urlpatterns = [
    path(
        "",
        homepage.views.Home.as_view(),
        name="home",
    ),
]
