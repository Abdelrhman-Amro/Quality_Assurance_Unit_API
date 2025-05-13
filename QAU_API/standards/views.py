import os

# Import course models
from courses.models import Course, CourseFile
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import AcademicYear, Attachment, Element, Pointer, Request, Standard
from .permissions import (
    IsAssignedToStandard,
    IsReceiver,
    IsRequester,
    IsSharedWithAttachment,
)
from .serializers import (
    AcademicYearSerializer,
    AttachmentSerializer,
    ElementSerializer,
    PointerSerializer,
    RequestDetailSerializer,
    RequestSerializer,
    StandardSerializer,
)


class AcademicYearViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AcademicYear model.
    Admin: Full CRUD operations
    Others: Read-only access

    Features:
    - Filter by status
    - Sort by start_date
    - Search by start_date, end_date
    - Pagination
    - Create new year based on latest year structure (Admin only)
    - View complete year structure (structure action)
    """

    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["start_date"]
    ordering_fields = ["start_date"]
    ordering = ["-start_date"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "repeat_schema", "create_new_year"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["get"])
    def structure(self, request, pk=None):
        """
        Get the complete hierarchical structure of an academic year.
        This includes all standards, pointers, elements, and courses,
        but excludes user information and actual file content.

        Returns:
        - standards: List of standards with their pointers and elements
        - courses: List of courses with their course files
        """
        academic_year = self.get_object()

        # Get all standards for this year with related objects
        standards_data = []
        standards = Standard.objects.filter(academic_year=academic_year)

        for standard in standards:
            standard_data = {"id": standard.id, "title": standard.title, "type": standard.type, "pointers": []}

            # Get pointers for this standard
            pointers = Pointer.objects.filter(standard=standard)
            for pointer in pointers:
                pointer_data = {"id": pointer.id, "title": pointer.title, "elements": []}

                # Get elements for this pointer
                elements = Element.objects.filter(pointer=pointer)
                for element in elements:
                    element_data = {"id": element.id, "title": element.title, "attachments": []}

                    # Get attachments for this element (excluding file content and user info)
                    attachments = Attachment.objects.filter(element=element)
                    for attachment in attachments:
                        element_data["attachments"].append({"id": attachment.id, "title": attachment.title, "has_file": bool(attachment.file)})

                    pointer_data["elements"].append(element_data)

                standard_data["pointers"].append(pointer_data)

            standards_data.append(standard_data)

        # Get all courses for this year with related objects
        courses_data = []
        courses = Course.objects.filter(academic_year=academic_year)

        for course in courses:
            course_data = {
                "id": course.id,
                "title": course.title,
                "code": course.code,
                "level": course.level,
                "semester": course.semester,
                "credit_hours": course.credit_hours,
                "department": course.department,
                "course_files": [],
            }

            # Get course files for this course (excluding file content and user info)
            course_files = CourseFile.objects.filter(course=course)
            for course_file in course_files:
                course_data["course_files"].append(
                    {"id": course_file.id, "title": course_file.title, "has_file": bool(course_file.file) if hasattr(course_file, "file") else False}
                )

            courses_data.append(course_data)

        # Combine the data
        structure_data = {
            "academic_year": {"id": academic_year.id, "start_date": academic_year.start_date, "end_date": academic_year.end_date, "status": academic_year.status},
            "standards": standards_data,
            "courses": courses_data,
        }

        return Response(structure_data)

    @action(detail=False, methods=["post"])
    def create_new_year(self, request):
        """
        Create a new academic year and automatically copy all structure (standards, pointers, elements)
        and courses (with course files) from the latest academic year.
        Does not copy attachment files or permissions.

        Required POST data:
        - start_date: Start date of new academic year (YYYY-MM-DD)
        - end_date: End date of new academic year (YYYY-MM-DD)
        - status: Status of new academic year (ACTIVE or ARCHIVED)
        """
        # Get the data for the new year
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Find the latest academic year to copy from
        latest_year = AcademicYear.objects.order_by("-start_date").first()
        if not latest_year:
            return Response(
                {"detail": "No existing academic year found to copy from."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create the new academic year
        new_academic_year = serializer.save()

        # Copy standards and their related objects
        standards_copied = self._copy_standards(latest_year, new_academic_year)

        # Copy courses and their related objects
        courses_copied = self._copy_courses(latest_year, new_academic_year)

        # Combine the copied counts
        copied_count = {**standards_copied, **courses_copied}

        return Response(
            {
                "detail": f"Successfully created new academic year {new_academic_year} with structure copied from {latest_year}.",
                "academic_year": serializer.data,
                "copied_count": copied_count,
            },
            status=status.HTTP_201_CREATED,
        )

    def _copy_standards(self, source_academic_year, target_academic_year):
        """Helper method to copy standards and related objects from source to target academic year."""
        copied_count = {
            "standards": 0,
            "pointers": 0,
            "elements": 0,
            "attachments": 0,
        }

        # Get all standards from source
        source_standards = Standard.objects.filter(academic_year=source_academic_year)

        for source_standard in source_standards:
            # Create new standard in target academic year
            new_standard = Standard.objects.create(
                academic_year=target_academic_year,
                title=source_standard.title,
                type=source_standard.type,
            )
            copied_count["standards"] += 1

            # Copy pointers
            source_pointers = Pointer.objects.filter(standard=source_standard)
            for source_pointer in source_pointers:
                new_pointer = Pointer.objects.create(
                    standard=new_standard,
                    title=source_pointer.title,
                )
                copied_count["pointers"] += 1

                # Copy elements
                source_elements = Element.objects.filter(pointer=source_pointer)
                for source_element in source_elements:
                    new_element = Element.objects.create(
                        pointer=new_pointer,
                        title=source_element.title,
                    )
                    copied_count["elements"] += 1

                    # Create empty attachment placeholders (no files or permissions)
                    source_attachments = Attachment.objects.filter(element=source_element)
                    for source_attachment in source_attachments:
                        Attachment.objects.create(
                            element=new_element,
                            title=source_attachment.title,
                        )
                        copied_count["attachments"] += 1

        return copied_count

    def _copy_courses(self, source_academic_year, target_academic_year):
        """Helper method to copy courses and course files from source to target academic year."""
        copied_count = {
            "courses": 0,
            "course_files": 0,
        }

        # Get all courses from source
        source_courses = Course.objects.filter(academic_year=source_academic_year)

        for source_course in source_courses:
            # Create new course in target academic year with same attributes except ID, academic_year
            # Note: We keep the same professor assignment
            new_course = Course.objects.create(
                academic_year=target_academic_year,
                professor=source_course.professor,
                title=source_course.title,
                code=f"{source_course.code}_{target_academic_year.start_date.year}",  # Make code unique for new year
                level=source_course.level,
                semester=source_course.semester,
                credit_hours=source_course.credit_hours,
                department=source_course.department,
            )
            copied_count["courses"] += 1

            # Copy course files
            source_course_files = CourseFile.objects.filter(course=source_course)
            for source_file in source_course_files:
                # Create empty course file (no attachments)
                new_file = CourseFile.objects.create(
                    course=new_course,
                    title=source_file.title,
                )
                copied_count["course_files"] += 1

                # Note: We do not copy CourseAttachments as they contain actual files

        return copied_count


class StandardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Standard model.
    Admin: Full CRUD operations
    Others: Read-only access

    Features:
    - Filter by type, academic_year
    - Sort by created_at
    - Search by title
    - Pagination
    """

    queryset = Standard.objects.all()
    serializer_class = StandardSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "academic_year"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class PointerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pointer model.
    Admin: Full CRUD operations
    Others: Read-only access

    Features:
    - Filter by standard
    - Sort by created_at
    - Search by title
    - Pagination
    """

    queryset = Pointer.objects.all()
    serializer_class = PointerSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["standard"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class ElementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Element model.
    Admin: Full CRUD operations
    Others: Read-only access

    Features:
    - Filter by pointer
    - Sort by created_at
    - Search by title
    - Pagination
    """

    queryset = Element.objects.all()
    serializer_class = ElementSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["pointer"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class AttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Attachment model.
    Admin: Full CRUD operations
    SUPERVISOR/TA: Upload/Remove if assigned to standard, Download if assigned or shared
    Others: Read-only access

    Features:
    - Filter by element
    - Sort by created_at
    - Search by title
    - Pagination
    """

    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["element"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        elif self.action == "upload":
            return [IsAuthenticated()]
        elif self.action == "remove":
            return [IsAuthenticated()]
        elif self.action == "download":
            # Custom permission handling in the download action
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        If a file is provided, set uploaded_by
        """
        file = self.request.FILES.get("file")
        if file:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        """
        If a file is provided, set uploaded_by
        """
        file = self.request.FILES.get("file")

        if file:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=["post", "get"])
    def upload(self, request, pk=None):
        """
        Upload an attachment file.
        Only users assigned to the standard can upload.
        """
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"detail": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attachment = self.get_object()
        standard = attachment.element.pointer.standard

        if attachment.file:
            return Response(
                {"detail": "Attachment already has a file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user in standard.assigned_to.all() or request.user.is_staff:
            attachment.file = file
            attachment.uploaded_by = request.user
            attachment.save()
            serializer = self.get_serializer(attachment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "You are not assigned to this standard."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=True, methods=["delete"])
    def remove(self, request, pk=None):
        """
        Remove an attachment file.
        Only users assigned to the standard or admins can remove.
        """
        attachment = self.get_object()
        standard = attachment.element.pointer.standard

        if request.user in standard.assigned_to.all() or request.user.is_staff:
            if attachment.file:
                attachment.file.delete(save=True)
            attachment.uploaded_by = None
            attachment.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "You are not assigned to this standard."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """
        Download an attachment file.
        Users can download if:
        1. They are assigned to the standard, or
        2. The attachment is shared with them, or
        3. They are admins
        """
        attachment = self.get_object()
        standard = attachment.element.pointer.standard

        # Check permissions
        if request.user in standard.assigned_to.all() or request.user in attachment.shared_with.all() or request.user.is_staff:

            if not attachment.file:
                return Response({"detail": "No file attached."}, status=status.HTTP_404_NOT_FOUND)

            file_path = os.path.join(settings.MEDIA_ROOT, attachment.file.name)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, "rb"))
                response["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"detail": "You do not have permission to download this file."},
            status=status.HTTP_403_FORBIDDEN,
        )


class RequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Request model.
    Admin: Full CRUD operations, Approve/Reject/Cancel
    SUPERVISOR/TA: Create if attachment has file and uploader,
                Retrieve/List their sent/received requests,
                Approve/Reject received requests (if not pending),
                Cancel sent requests (if not pending)

    Features:
    - Filter by status, requester, receiver
    - Sort by created_at
    - Search by requester, receiver
    - Pagination
    """

    queryset = Request.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "requester", "receiver"]
    search_fields = ["requester__username", "receiver__username"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RequestDetailSerializer
        return RequestSerializer

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        elif self.action == "approve" or self.action == "reject":
            return [IsAuthenticated(), IsReceiver()]
        elif self.action == "cancel":
            return [IsAuthenticated(), IsRequester()]
        return [IsAdminUser()]

    def get_queryset(self):
        """
        Filter requests based on user role:
        - Admin: All requests
        - Others: Only their sent or received requests
        """
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset

        return queryset.filter(requester=user) | queryset.filter(receiver=user)

    def perform_create(self, serializer):
        """
        Before Create:
            - Set requester to current user.
            - Set receiver based on attachment.
        """
        attachment = serializer.validated_data.get("made_on")

        serializer.save(
            requester=self.request.user,
            receiver=attachment.uploaded_by,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        Approve a request.
        Only the receiver or admin can approve a request.
        """
        req = self.get_object()

        if req.status != Request.Status.PENDING:
            return Response(
                {"detail": f"Cannot approve a request with status '{req.get_status_display()}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        req.status = Request.Status.APPROVED
        req.save()

        # Add requester to shared_with list of the attachment
        if req.made_on:
            req.made_on.shared_with.add(req.requester)

        serializer = self.get_serializer(req)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """
        Reject a request.
        Only the receiver or admin can reject a request.
        """
        req = self.get_object()

        if req.status != Request.Status.PENDING:
            return Response(
                {"detail": f"Cannot reject a request with status '{req.get_status_display()}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        req.status = Request.Status.REJECTED
        req.save()

        serializer = self.get_serializer(req)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        Cancel a request.
        Only the requester or admin can cancel a request.
        """
        req = self.get_object()

        if req.status != Request.Status.PENDING:
            return Response(
                {"detail": f"Cannot cancel a request with status '{req.get_status_display()}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        req.status = Request.Status.CANCELED
        req.save()

        serializer = self.get_serializer(req)
        return Response(serializer.data)
