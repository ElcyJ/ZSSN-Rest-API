from rest_framework import permissions

class ReadOnly(permissions.BasePermission):
    message = 'Changing inventory items not allowed'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
        