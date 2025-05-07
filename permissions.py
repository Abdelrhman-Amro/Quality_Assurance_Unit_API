# from rest_framework import permissions


# class IsAdminUser(permissions.BasePermission):
#     """Permission to check if user is admin"""

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "ADMIN"


# class IsSupervisorOrTAOrProfessor(permissions.BasePermission):
#     """Permission to check if user is supervisor, TA, or professor"""

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in [
#             "SUPERVISOR",
#             "TA",
#             "PROFESSOR",
#         ]


# class IsSupervisorOrTA(permissions.BasePermission):
#     """Permission to check if user is supervisor or TA"""

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in [
#             "SUPERVISOR",
#             "TA",
#         ]


# class IsOwnerOrAdmin(permissions.BasePermission):
#     """Permission to check if user is owner of the attachment or admin"""

#     def has_object_permission(self, request, view, obj):
#         return request.user.role == "ADMIN" or obj.uploaded_by == request.user


# class IsRequesterOrReceiverOrAdmin(permissions.BasePermission):
#     """Permission to check if user is requester, receiver, or admin"""

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.user.role == "ADMIN"
#             or obj.requester == request.user
#             or obj.receiver == request.user
#         )
