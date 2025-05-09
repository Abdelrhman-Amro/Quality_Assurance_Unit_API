from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    """
    Permission to check if user has ADMIN role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.ADMIN


class IsSupervisor(permissions.BasePermission):
    """
    Permission to check if user has SUPERVISOR role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.SUPERVISOR


class IsProfessor(permissions.BasePermission):
    """
    Permission to check if user has PROFESSOR role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.PROFESSOR


class IsTa(permissions.BasePermission):
    """
    Permission to check if user has TA role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.TA


class IsCourseProfessor(permissions.BasePermission):
    """
    Permission to check if user is a course  professor.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and is the professor of the course
        return request.user.is_authenticated and obj.professor == request.user
