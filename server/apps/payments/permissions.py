from rest_framework import permissions
from rest_framework.request import Request


class IsPaymentOnwer(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True
    
    def has_object_permission(self, request: Request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
