from rest_framework import permissions
from django.http import HttpRequest
from typing import Any


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Admin permissions
        if request.user.is_staff:
            return True

        # Instance must have an attribute named `user`
        return obj.user == request.user


class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: Any, obj: Any) -> bool:
        return obj.user == request.user


class CanManageOrders(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: Any) -> bool:
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.has_perm("orders.can_manage_orders")
        )
