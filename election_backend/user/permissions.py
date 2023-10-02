from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        permissions_required = getattr(view, 'permissions_required', None)
        return request.user.has_perms(permissions_required.get(request.method))
