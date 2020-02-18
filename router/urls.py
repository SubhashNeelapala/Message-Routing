from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('message_routing.urls')),
]