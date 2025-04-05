from rest_framework.permissions import BasePermission


class IsAdminOrSelfDelete(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True  # open registration
        if view.action == "destroy":
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj == request.user or request.user.is_staff
        return request.user and request.user.is_staff
