from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AcademicYearViewSet,
    AttachmentViewSet,
    ElementViewSet,
    PointerViewSet,
    RequestViewSet,
    StandardViewSet,
)

router = DefaultRouter()
router.register(r"academic-years", AcademicYearViewSet)
router.register(r"standards", StandardViewSet)
router.register(r"pointers", PointerViewSet)
router.register(r"elements", ElementViewSet)
router.register(r"attachments", AttachmentViewSet)
router.register(r"requests", RequestViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
