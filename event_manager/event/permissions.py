from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user
