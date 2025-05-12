import os

from django.conf import settings
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Course, CourseAttachment, CourseFile
from .permissions import IsProfessorOfCourse
from .serializers import (
    CourseAttachmentSerializer,
    CourseFileSerializer,
    CourseSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model.
    Admin: Full CRUD operations
    Others: Read-only access

    Features:
    - Filter by academic_year, level, semester
    - Sort by created_at
    - Search by title
    - Pagination
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["academic_year", "level", "semester", "department"]
    search_fields = ["title", "code"]
    ordering_fields = ["created_at", "title", "credit_hours", "department"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class CourseFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CourseFile model.
    Admin: Full CRUD operations
    Others: Read-only access

    Features:
    - Filter by course
    - Sort by created_at
    - Search by title
    - Pagination
    """

    queryset = CourseFile.objects.all()
    serializer_class = CourseFileSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["course"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class CourseAttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CourseAttachment model.
    Admin: Full CRUD operations
    PROFESSOR: Upload/Remove/Download their own course attachments
    Others: Read-only access

    Features:
    - Filter by course_file
    - Sort by created_at
    - Pagination
    """

    queryset = CourseAttachment.objects.all()
    serializer_class = CourseAttachmentSerializer
    permission_classes = [IsProfessorOfCourse | IsAdminUser]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course_file"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [IsAuthenticated()]

        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """
        Download a course attachment file.
        """
        attachment = self.get_object()
        file_path = os.path.join(settings.MEDIA_ROOT, attachment.file.name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, "rb"))
            response["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
