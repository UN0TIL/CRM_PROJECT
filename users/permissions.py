from rest_framework import permissions

from .roles import Roles


class CustomObjectPermissions(permissions.BasePermission):

    edit_methods = ('PUT', 'PATCH', 'GET')

    def has_permission(self, request, view):
        if request.user.role == Roles.ADMIN:
            return True
        
        elif request.user.role == Roles.MANAGER:
            return True

        elif request.user.role == Roles.CLIENT:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == Roles.ADMIN:
            return True
        
        elif request.user.role == Roles.MANAGER:
            return True

        elif request.user.role == Roles.CLIENT:
            return True
        
        return False