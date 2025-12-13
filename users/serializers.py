from rest_framework import serializers

from .models import Order, Client
from .choices import OrderStatus

class AdminManagerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'name', 'description', 'status', 'price', 'created_at', 'updated_at']

class ClientOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'name', 'description', 'status', 'price', 'created_at']

class AdminManagerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  
        fields = ['id', 'name', 'email', 'phone', 'is_active', 'manager', 'orders']

class ClientClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  
        fields = ['id', 'name', 'email', 'orders']

class OrderChangeStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)