from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += (
        path(
            "__debug__/",
            include("debug_toolbar.urls"),
        ),
    )

if settings.MEDIA_ROOT:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=(settings.MEDIA_ROOT),
    )
