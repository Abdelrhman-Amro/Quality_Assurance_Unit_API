from django.urls import include, path
from rest_framework import routers

from .views import UserRetrieveView, UserViewSet

router = routers.SimpleRouter()

router.register(r"users", UserViewSet)

urlpatterns = [
    path("user/", UserRetrieveView.as_view(), name="user-detail"),
    path("", include(router.urls)),
]
