from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path(
        "api/",
        include(
            [
                path("users", include("user.urls")),
                path("organisations/", include("organisation.urls")),
            ]
        ),
    ),
]
