from django.shortcuts import render
from rest_framework import viewsets

from .permissions import CustomObjectPermissions
from .models import Order
from .roles import Roles

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomObjectPermissions]          

    def get_queryset(self):
        user = self.request.user

        if user.role == Roles.ADMIN:
            return Order.objects.all()
        elif user.role == Roles.MANAGER:
            return Order.objects.filter(client__manager=user)
        elif user.role == Roles.CLIENT:
            return Order.objects.filter(client__user=user)