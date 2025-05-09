from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseAttachmentViewSet, CourseFileViewSet, CourseViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"course-files", CourseFileViewSet)
router.register(r"course-attachments", CourseAttachmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
