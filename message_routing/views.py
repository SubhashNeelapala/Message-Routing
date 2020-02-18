from django.shortcuts import render
from .models import IpAddress,Gateway,Prefix
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from message_routing.serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404




class CreateGateway(APIView):
    def get(self,request):
        serializer = GatewayCreateSerializer()
        return Response(serializer.data)
    def post(self,request):
        serializer = GatewayCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                gateway_obj = Gateway.objects.get(name=request.data['name'])
                message = {"message":"gateway with samename already exist","param":request.data['name'],"status":400}
                return Response(message)
            except Exception as e:
                name=request.data['name']
                ip_address = request.data['ip_address']
                gateway_obj = Gateway.objects.create(name=name)
                for each in ip_address:
                    try:
                        ip_address_obj = IpAddress.objects.get(address=each)
                        return Response({"message":"Ip Address Already exist"})
                    except Exception as e:
                        ip_address_obj = IpAddress.objects.create(address=each)
                    gateway_obj.ip_address.add(ip_address_obj)
                response={"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
                return Response(response)
                # response = gateway_obj.values('id',)

        else:            
            context_data = {"success" : False, "errors" : {"message":serializer.errors}}
        return Response(context_data)


class GetGatewayDetails(APIView):
    def get(self,request,id=None):
        print( "sdfsdfsdfsdf")
        if id is not None:
            gateway_obj = get_object_or_404(Gateway, id=id)
            response={"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
            return Response(response)

class CreateRouteMapping(APIView):
    def post(self,request):
        serializer = RouteCreateSerializer(data=request.data)
        if serializer.is_valid():
            gateway_id = request.data['gateway_id']
            prefix_name = request.data['prefix_name']
            try:
                gateway_obj = Gateway.objects.get(id=gateway_id)
                try:
                    prefix_obj = Prefix.objects.get(gateway=gateway_obj,prefix_name=prefix_name)
                    response={"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
                    return Response(response)
                except Exception as e:
                    print("before except")
                    prefix_obj = Prefix.objects.create(gateway=gateway_obj,prefix_name=prefix_name)
                    gateway_details = {"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
                    response = {"id":prefix_obj.id,"prefix":prefix_obj.prefix_name,"gateway":gateway_details}
                    return Response(response)

            except Exception as e:
                return Response({"status":400,"message":"No Gateway found with the given id"})
        else:            
            context_data = {"message":serializer.errors}
            return Response(context_data)

class GetRouteMapping(APIView):
    def get(self,request,unique_route_id):
        if unique_route_id is not None:
            try:
                prefix_obj = Prefix.objects.get(id=unique_route_id)
                print (prefix_obj.gateway,"999999999999")
                gateway_obj = Gateway.objects.get(id=prefix_obj.gateway.id)
                gateway_details = {"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
                response = {"id":prefix_obj.id,"prefix":prefix_obj.prefix_name,"gateway":gateway_details}
                return Response(response)
            except Exception as e:
                return Response({"status":404,"message":"No Record Found"})
        else:
            return Response({"message":"please enter a unique route id"})



class SearchGatewayNumber(APIView):
    def get(self,request,number=None):
        if number is not None:
            first_four_digits = int(str(number)[:4])
            first_three_digits = int(str(number)[:3])
            try:
                prefix_obj = Prefix.objects.get(prefix_name=first_four_digits)
                gateway_obj = Gateway.objects.get(id=prefix_obj.gateway.id)
                gateway_details = {"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
                response = {"id":prefix_obj.id,"prefix":prefix_obj.prefix_name,"gateway":gateway_details}
                return Response(response)

            except Prefix.DoesNotExist as e:
                prefix_obj = Prefix.objects.get(prefix_name=first_three_digits)
                gateway_obj = Gateway.objects.get(id=prefix_obj.gateway.id)
                gateway_details = {"id":gateway_obj.id,"name":gateway_obj.name,"ip_addresses":[ip_address.address for ip_address in gateway_obj.ip_address.all()]}
                response = {"id":prefix_obj.id,"prefix":prefix_obj.prefix_name,"gateway":gateway_details}
                return Response(response)
            except Exception as e:
                message = {"message":"gateway with samename already exist","param":number,"status":400}
                return Response(message)
                




