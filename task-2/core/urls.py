from django.urls import path, include, re_path

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path(
        "api/",
        include(
            [
                path("users/", include("user.urls")),
                re_path(r"^organisations/?", include("organisation.urls")),
            ]
        ),
    ),
]
