from rest_framework import serializers

from .models import Order, Client

class AdminManagerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'name', 'discription']

class ClientOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'name', 'discription']

class AdminManagerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  
        fields = ['id', 'user', 'manager']

class ClientClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client  
        fields = ['id', 'user']
