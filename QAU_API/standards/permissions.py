from rest_framework import permissions


class IsSharedWithAttachment(permissions.BasePermission):
    """
    Permission to check if user exists in attachment's shared_with list.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and exists in the attachment's shared_with
        return request.user.is_authenticated and request.user in obj.shared_with.all()


class IsAssignedToStandard(permissions.BasePermission):
    """
    Permission to check if user exists in standard's assigned_to list.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and exists in the standard's assigned_to
        return request.user.is_authenticated and request.user in obj.assigned_to.all()


class IsRequester(permissions.BasePermission):
    """
    Permission to check if user is the one who sent the request.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and is the requester
        return request.user.is_authenticated and request.user == obj.requester


class IsReceiver(permissions.BasePermission):
    """
    Permission to check if user is the one who received the request.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and is the receiver
        return request.user.is_authenticated and request.user == obj.receiver
