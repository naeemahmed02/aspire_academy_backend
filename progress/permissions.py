class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return obj.student == request.user