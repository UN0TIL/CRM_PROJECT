from rest_framework import permissions
from rest_framework.viewsets import ViewSet
from django.http import HttpRequest

from .choices import Roles
from .models import Order, Client


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view: ViewSet):

        return (
            request.user.is_authenticated
            and request.user.role == Roles.ADMIN
        )

class IsManager(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view: ViewSet):

        return (
            request.user.is_authenticated
            and request.user.role == Roles.MANAGER
        )
    
class IsClientReadOnly(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view: ViewSet):

        return (
            request.user.is_authenticated
            and request.user.role == Roles.CLIENT
            and request.method in permissions.SAFE_METHODS
        )

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: ViewSet, obj: Order|Client):
        user = request.user

        if user.role == Roles.ADMIN:
            return True

        if user.role == Roles.MANAGER:
            if isinstance(obj, Order):
                return obj.client.manager == request.user
            if isinstance(obj, Client):
                return obj.manager == request.user

        if user.role == Roles.CLIENT:
            if isinstance(obj, Order):
                return obj.client.user == request.user
            if isinstance(obj, Client):
                return obj.user == request.user

        return False