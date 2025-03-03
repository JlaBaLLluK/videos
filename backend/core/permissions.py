from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUserItself(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.id == obj.id


class IsObjectOwnerOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.id == obj.author.id
