from django.conf.urls import include, url
from .views import *

urlpatterns = [
    # path('', views.index, name='index'),
   	url(r'^gateway/$', CreateGateway.as_view(),name='create_gateway'),
   	url(r'^gateway/(?P<id>\d+)$', GetGatewayDetails.as_view(),name='get_gateway'),
   	url(r'^route/$', CreateRouteMapping.as_view(),name='create_route'),
   	url(r'^route/(?P<unique_route_id>\d+)$', GetRouteMapping.as_view(),name='apping_route'),
   	url(r'^search/route/(?P<number>\d+)$', SearchGatewayNumber.as_view(),name='get_number_gatway'),
    
]
