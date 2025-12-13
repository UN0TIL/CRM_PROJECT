from django.urls import path, include
from rest_framework import routers

from .views import OrderViewSet, ClientViewSet

app_name = 'users'

users_router = routers.DefaultRouter()

users_router.register('orders', OrderViewSet, basename='orders')
users_router.register('clients', ClientViewSet, basename='clients')

urlpatterns = [
    path('', include(users_router.urls))
]
