from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from .roles import Roles

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):        
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email=email)

        role = extra_fields.get("role", Roles.CLIENT)

        if role == Roles.CLIENT and extra_fields.get('is_staff'):
            role = Roles.MANAGER

        extra_fields.setdefault('role', role)

        user = self.model(email=email, **extra_fields)

        permission = self._users_role(role)

        if permission:
            user.user_permissions.add(permission)

        user.set_password(password)
        user.save()

        return user
        
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        role = Roles.ADMIN
        extra_fields.setdefault('role', role)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
    @staticmethod
    def _users_role(role):
        permission = None
        if role == Roles.CLIENT:
            permission = Permission.objects.get(codename='view_self')
        elif role == Roles.MANAGER:
            permission = Permission.objects.get(codename='view_only_own')

        return permission