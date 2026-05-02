from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_staff or
                request.user.groups.filter(name__in=['Teacher', 'Admin']).exists()
            )
        )


class IsStudentReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Students can only read
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return False



from rest_framework.permissions import BasePermission

class AnnouncementPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated and (
                request.user.is_staff or
                request.user.groups.filter(name__in=['Teacher', 'Admin']).exists()
            )
        )