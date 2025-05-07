# from django.http import FileResponse
# from django.shortcuts import get_object_or_404
# from rest_framework import permissions, status, viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from .models import AcademicYear, Attachment, Element, Pointer, Request, Standard
# from .permissions import (
#     IsAdminUser,
#     IsOwnerOrAdmin,
#     IsRequesterOrReceiverOrAdmin,
#     IsSupervisorOrTA,
#     IsSupervisorOrTAOrProfessor,
# )
# from .serializers import (
#     AcademicYearSerializer,
#     AttachmentSerializer,
#     ElementSerializer,
#     PointerSerializer,
#     RequestSerializer,
#     StandardSerializer,
# )


# class AcademicYearViewSet(viewsets.ModelViewSet):
#     queryset = AcademicYear.objects.all()
#     serializer_class = AcademicYearSerializer

#     def get_permissions(self):
#         if self.action in ["list", "retrieve"]:
#             permission_classes = [permissions.IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


# class StandardViewSet(viewsets.ModelViewSet):
#     queryset = Standard.objects.all()
#     serializer_class = StandardSerializer

#     def get_permissions(self):
#         if self.action in ["list", "retrieve"]:
#             permission_classes = [permissions.IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


# class PointerViewSet(viewsets.ModelViewSet):
#     queryset = Pointer.objects.all()
#     serializer_class = PointerSerializer

#     def get_permissions(self):
#         if self.action in ["list", "retrieve"]:
#             permission_classes = [permissions.IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


# class ElementViewSet(viewsets.ModelViewSet):
#     queryset = Element.objects.all()
#     serializer_class = ElementSerializer

#     def get_permissions(self):
#         if self.action in ["list", "retrieve"]:
#             permission_classes = [permissions.IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


# class AttachmentViewSet(viewsets.ModelViewSet):
#     queryset = Attachment.objects.all()
#     serializer_class = AttachmentSerializer

#     def get_permissions(self):
#         if self.action in ["list", "retrieve"]:
#             permission_classes = [permissions.IsAuthenticated]
#         elif self.action in ["create", "update", "partial_update", "destroy"]:
#             permission_classes = [IsAdminUser | IsOwnerOrAdmin]
#         elif self.action == "download":
#             permission_classes = [permissions.IsAuthenticated]
#         elif self.action == "upload":
#             permission_classes = [IsSupervisorOrTA | IsAdminUser]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]

#     def perform_create(self, serializer):
#         serializer.save(uploaded_by=self.request.user)

#     @action(detail=True, methods=["get"])
#     def download(self, request, pk=None):
#         attachment = self.get_object()
#         # Check if user has access to this attachment
#         if (
#             request.user.role == "ADMIN"
#             or attachment.uploaded_by == request.user
#             or request.user in attachment.shared_with.all()
#         ):
#             file_handle = attachment.file.open()
#             response = FileResponse(
#                 file_handle, content_type="application/octet-stream"
#             )
#             response["Content-Disposition"] = (
#                 f'attachment; filename="{attachment.file.name}"'
#             )
#             return response
#         else:
#             return Response(
#                 {"detail": "You do not have permission to download this file."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     @action(detail=True, methods=["post"])
#     def upload(self, request, pk=None):
#         attachment = self.get_object()
#         # Check if user is the owner or admin
#         if request.user.role == "ADMIN" or attachment.uploaded_by == request.user:
#             if "file" in request.FILES:
#                 attachment.file = request.FILES["file"]
#                 attachment.save()
#                 return Response(
#                     {"detail": "File uploaded successfully."}, status=status.HTTP_200_OK
#                 )
#             return Response(
#                 {"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
#             )
#         else:
#             return Response(
#                 {"detail": "You do not have permission to upload to this attachment."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )


# class RequestViewSet(viewsets.ModelViewSet):
#     queryset = Request.objects.all()
#     serializer_class = RequestSerializer

#     def get_permissions(self):
#         if self.action in ["create"]:
#             permission_classes = [IsSupervisorOrTA]
#         elif self.action in ["list", "retrieve"]:
#             permission_classes = [permissions.IsAuthenticated]
#         elif self.action in ["update", "partial_update", "destroy"]:
#             permission_classes = [IsAdminUser | IsRequesterOrReceiverOrAdmin]
#         elif self.action in ["approve", "reject"]:
#             permission_classes = [IsAdminUser | permissions.IsAuthenticated]
#         elif self.action == "cancel":
#             permission_classes = [IsAdminUser | permissions.IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]

#     def perform_create(self, serializer):
#         serializer.save(requester=self.request.user, status=Request.Status.PENDING)

#     def get_queryset(self):
#         user = self.request.user
#         if user.role == "ADMIN":
#             return Request.objects.all()
#         return Request.objects.filter(requester=user) | Request.objects.filter(
#             receiver=user
#         )

#     @action(detail=True, methods=["post"])
#     def approve(self, request, pk=None):
#         req = self.get_object()
#         # Check if user is the receiver or admin
#         if request.user.role == "ADMIN" or req.receiver == request.user:
#             req.status = Request.Status.APPROVED
#             req.save()
#             # Add requester to shared_with of the attachment
#             if req.made_on:
#                 req.made_on.shared_with.add(req.requester)
#             return Response(
#                 {"detail": "Request approved successfully."}, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {"detail": "You do not have permission to approve this request."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     @action(detail=True, methods=["post"])
#     def reject(self, request, pk=None):
#         req = self.get_object()
#         # Check if user is the receiver or admin
#         if request.user.role == "ADMIN" or req.receiver == request.user:
#             req.status = Request.Status.REJECTED
#             req.save()
#             return Response(
#                 {"detail": "Request rejected successfully."}, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {"detail": "You do not have permission to reject this request."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     @action(detail=True, methods=["post"])
#     def cancel(self, request, pk=None):
#         req = self.get_object()
#         # Check if user is the requester or admin
#         if request.user.role == "ADMIN" or req.requester == request.user:
#             req.status = Request.Status.CANCELED
#             req.save()
#             return Response(
#                 {"detail": "Request canceled successfully."}, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {"detail": "You do not have permission to cancel this request."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )
