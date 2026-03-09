from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to authenticated users,
    but only admins can create/update/delete.
    """

    def has_permission(self, request, view):

        # Allow GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # Write permissions only for admins
        return request.user and request.user.is_staff