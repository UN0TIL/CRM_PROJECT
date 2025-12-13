from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from .choices import Roles, OrderStatus
from .manager import CustomUserManager
from .validators import validate_phone_number

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('Email address'), unique=True)
    role = models.CharField(_('Role'), choices=Roles.choices, default=Roles.CLIENT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(_('Client email address'))
    phone = models.CharField(max_length=20, blank=True, validators=[validate_phone_number])
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients',
        limit_choices_to={'role': Roles.MANAGER}
    )

    def __str__(self):
        return f'Client: {self.name}'

class Order(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        limit_choices_to={'role': Roles.MANAGER}
    )
    name = models.CharField(_('Name'), max_length=40)
    description = models.TextField(_('Description'))

    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    status = models.CharField(_("Status"), max_length=30, choices=OrderStatus.choices, default=OrderStatus.DRAFT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.name} by {self.client}'
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    method = models.CharField(max_length=40, choices=)