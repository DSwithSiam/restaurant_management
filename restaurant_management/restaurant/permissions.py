from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_employee and request.user.restaurant == obj.restaurant