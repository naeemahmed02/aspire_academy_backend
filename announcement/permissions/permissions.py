from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_staff or
                request.user.groups.filter(name__in=['Teacher', 'Admin']).exists()
            )
        )


class IsAuthenticatedReadOnly(BasePermission):
    """
    Any authenticated user can read, no one can write.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS and request.user.is_authenticated