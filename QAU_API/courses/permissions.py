from rest_framework import permissions


class IsProfessorOfCourse(permissions.BasePermission):
    """
    Permission to check if user is the professor assigned to the course.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and is the professor of the course
        return request.user.is_authenticated and request.user == obj.course_file.course.professor
