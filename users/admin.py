from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Order, Client
from .forms import UserChangeForm, UserCreateForm

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    ordering = 'email',
    list_display = ('email', 'role', 'is_active', 'is_staff')
    add_form = UserCreateForm
    form = UserChangeForm

    fieldsets = (
    (None, {
        'fields': (
            'email',
            'role',
            'is_active',
            'is_staff',
            )
        }),
    )
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': (
            'email',
            'role',
            'is_active',
            'is_staff',
            'password1',
            'password2',
            ),
        }),
    )


@admin.register(Client, Order)
class OrderAdmin(admin.ModelAdmin):
    pass