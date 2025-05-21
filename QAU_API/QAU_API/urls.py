from courses.views import CourseAttachmentViewSet, CourseFileViewSet, CourseViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from standards.views import (
    AcademicYearViewSet,
    AttachmentViewSet,
    ElementViewSet,
    PointerViewSet,
    RequestViewSet,
    StandardViewSet,
)
from users.views import UserViewSet

router = DefaultRouter()

# users app
router.register(r"users", UserViewSet)

# standards app
router.register(r"academic-years", AcademicYearViewSet)
router.register(r"standards", StandardViewSet)
router.register(r"pointers", PointerViewSet)
router.register(r"elements", ElementViewSet)
router.register(r"attachments", AttachmentViewSet)
router.register(r"requests", RequestViewSet)

# courses app
router.register(r"courses", CourseViewSet)
router.register(r"course-files", CourseFileViewSet)
router.register(r"course-attachments", CourseAttachmentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("users.auth")),
    path("api/", include("QAU_API.swagger")),
]

# This is for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
