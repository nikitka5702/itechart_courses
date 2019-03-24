from typing import Any

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsSuper(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_superuser

    def has_object_permission(self, request: Request, view: View, obj: Any):
        return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_staff

    def has_object_permission(self, request: Request, view: View, obj: Any):
        return request.user.is_staff


class StaffReadonly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_staff and request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.is_staff and request.method in permissions.SAFE_METHODS


class AuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.method in permissions.SAFE_METHODS
