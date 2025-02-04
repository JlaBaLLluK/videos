from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular import views as spectacular_views

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
    path("swagger/", spectacular_views.SpectacularSwaggerView.as_view()),
    path("schema/", spectacular_views.SpectacularAPIView.as_view(), name="schema"),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
