from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsPaymentOnwer(permissions.BasePermission):  # type: ignore[misc]
    """Permission to allow only payment owners to modify payments."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user is authenticated for general view access."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any,  # noqa: WPS110
    ) -> bool:
        """Check object-level permission."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.user == request.user)
