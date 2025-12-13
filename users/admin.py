from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Order, Client
from .forms import UserChangeForm, UserCreateForm
from .choices import OrderStatus
from ..services.order_service import OrderService

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

@admin.action(description='Mark as paid')
def mark_as_paid(modeladmin, request, queryset):
    for order in queryset:
        OrderService.change_status(
            order=order,
            new_status=OrderStatus.PAID,
            user=request.user
        )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class OrderAdmin(admin.ModelAdmin):
    pass