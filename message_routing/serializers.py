from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets



class GatewayCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    ip_address = serializers.ListField()

class RouteCreateSerializer(serializers.Serializer):
	prefix_name= serializers.CharField(max_length=100)
	gateway_id = serializers.CharField(max_length=100)