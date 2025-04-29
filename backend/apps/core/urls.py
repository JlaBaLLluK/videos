from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("users", views.UserViewSet)

urlpatterns = [
    path("search/", views.SearchView.as_view(), name="search"),
] + router.urls
