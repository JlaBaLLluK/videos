from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

api_v1_urls = [
    path(
        "auth/",
        include(
            [
                path("login/", jwt_views.token_obtain_pair),
                path("logout/", jwt_views.token_blacklist),
                path("refresh-token/", jwt_views.token_refresh),
                path("verify-token/", jwt_views.token_verify),
            ],
        ),
    ),
    path("core/", include("core.urls")),
]

urlpatterns = [
    path(
        "api/",
        include(
            [
                path("v1/", include(api_v1_urls)),
            ]
        ),
    ),
]
