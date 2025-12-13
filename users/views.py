from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .permissions import IsAdmin, IsClientReadOnly, IsManager, IsOwner
from .serializers import (
    AdminManagerOrderSerializer,
    AdminManagerClientSerializer,
    ClientClientSerializer,
    ClientOrderSerializer,
    OrderChangeStatusSerializer
)
from .models import Order, Client
from .choices import Roles
from ..services.order_service import OrderService


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):

    permission_classes = [
        IsAdmin | IsManager | IsClientReadOnly,
        IsOwner,
    ]

    def get_serializer_class(self):
        user = self.request.user

        if user.role == Roles.ADMIN:
            return AdminManagerOrderSerializer
        elif user.role == Roles.MANAGER:
            return AdminManagerOrderSerializer
        elif user.role == Roles.CLIENT:
            return ClientOrderSerializer
        else:
            return serializers.Serializer
        

    def get_queryset(self):
        user = self.request.user

        if user.role == Roles.ADMIN:
            return Order.objects.all()
        elif user.role == Roles.MANAGER:
            return Order.objects.filter(client__manager=user)
        elif user.role == Roles.CLIENT:
            return Order.objects.filter(client__user=user)
        else:
            return Order.objects.none()

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        order = self.get_object()

        serializer = OrderChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            OrderService.change_status(
                order=order,
                new_status=serializer.validated_data['status'],
                user=request.user,
            )
        except ValidationError as e:
            raise serializers.ValidationError(e.message)

        return Response({'status': order.status})


class ClientViewSet(viewsets.ModelViewSet):

    permission_classes = [
        IsAdmin | IsManager | IsClientReadOnly,
        IsOwner,
    ]

    def get_serializer_class(self):
        user = self.request.user

        if user.role == Roles.ADMIN:
            return AdminManagerClientSerializer
        elif user.role == Roles.MANAGER:
            return AdminManagerClientSerializer
        elif user.role == Roles.CLIENT:
            return ClientClientSerializer
        else:
            return serializers.Serializer

    def get_queryset(self):
        user = self.request.user

        if user.role == Roles.ADMIN:
            return Client.objects.all()
        elif user.role == Roles.MANAGER:
            return Client.objects.filter(manager=user)
        elif user.role == Roles.CLIENT:
            return Client.objects.filter(user=user)
        else:
            return Client.objects.none()

    @action(detail=False, methods=['get'], url_path='me')
    def client_profile_page(self, request):
        user = request.user

        if user.role != Roles.CLIENT:
            raise PermissionDenied
        
        client = Client.objects.get(user=user)
        serializers = ClientClientSerializer(client)
        return Response(serializers.data, status=status.HTTP_200_OK)