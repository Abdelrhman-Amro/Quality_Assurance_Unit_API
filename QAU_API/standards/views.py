import os

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
    """

    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["start_date"]
    ordering_fields = ["start_date"]
    ordering = ["-start_date"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


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

    @action(detail=True, methods=["post"])
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
