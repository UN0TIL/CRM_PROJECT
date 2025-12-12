from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .roles import Roles
from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('Email address'), unique=True)
    role = models.CharField(_('Role'), max_length=20, choices=Roles.choices, default=Roles.CLIENT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients',
        limit_choices_to={'role': Roles.MANAGER}
    )

    # def __str__(self):
    #     return self.user

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    discription = models.CharField(max_length=300)