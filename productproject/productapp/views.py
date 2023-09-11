from django.shortcuts import render
from .models import PlatformApiCall
from rest_framework import generics
from .models import Orders,Product
from .serializers import OrdersSerializer,ProductSerializer,UserSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
import json
from rest_framework.views import APIView

from django.db.models import Q
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from functools import wraps
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,CreateModelMixin,DestroyModelMixin,UpdateModelMixin



class PlatformApiMixin(ListModelMixin,RetrieveModelMixin,CreateModelMixin):
    def get_queryset(self):
        print(f"mixin called for qs {self.request.method}")
        # queryset = 
    
        PlatformApiCall.objects.create(
                user=self.request.user,
                requested_url=self.request.build_absolute_uri(),
                requested_data={"request_type":self.request.method,"query_param":str(self.request.GET),"request body":self.request.data},
                response_data=str(self.queryset)
            )
            # print(self.queryset)
        return super().get_queryset()
    def list(self, request, *args, **kwargs):
        print(f"mixin called for list {self.request.method}")
        # queryset = self.get_queryset()
            
        PlatformApiCall.objects.create(
                user=self.request.user,
                requested_url=self.request.build_absolute_uri(),
                requested_data={"request_type":self.request.method,"query_param":str(self.request.GET),"request body":self.request.data},
                response_data=str(self.queryset)
            )
            # print(self.queryset)
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        print(f"mixin called for create {self.request.method}")
        queryset = super().get_queryset()
            
        PlatformApiCall.objects.create(
                user=self.request.user,
                requested_url=self.request.build_absolute_uri(),
                requested_data={"request_type":self.request.method,"query_param":str(self.request.GET),"request body":self.request.data},
                response_data=str(queryset)
            )
            # print(self.queryset)
        return super().create(request, *args, **kwargs)

class RegisterUserView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created succesfuly"})
        return Response(serializer.errors)
    


class ProductListCreateView(PlatformApiMixin,generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    queryset = Product.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def create(self, request, *args, **kwargs):
        # Call the mixin's get_queryset method
        self.get_queryset()
        
        response = super().create(request, *args, **kwargs)
        return response
    
   
class ProductRetrieveUpdateDestroyView(PlatformApiMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]


def customer_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # print("user",request.request.user.id)
        user = request.request.user
        print("userid",user.id)
        orders = view_func(request, *args, **kwargs)
        # print("req",request.request,args,kwargs)

        # Check if the user is a customer and owns the orders
        if user.is_authenticated:
            orders = orders.filter(customer__user=user.id)

        return orders

    return _wrapped_view

class OrdersListCreateView(PlatformApiMixin,generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['id']

    @customer_only
    def get_queryset(self):
        queryset = Orders.objects.all()
        print("user gs",self.request.user)

        product_name = self.request.query_params.get('name')
        if product_name is not None:
            queryset = Orders.objects.select_related('customer').all()
            # .filter(products__name=product_name
            # )

        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.prefetch_related('products').filter(products__name__icontains=search_query)

        ascending_query = self.request.query_params.get('ascending')
        if ascending_query:
            queryset=queryset.order_by(ascending_query)

        descending_query = self.request.query_params.get('descending')
        if descending_query:
            queryset=queryset.order_by('-'+descending_query)

        limit_query = self.request.query_params.get('limit')
        if limit_query:
            queryset=queryset[:int(limit_query)]

        return queryset
    # def list(self, request, *args, **kwargs):
    #     print("inside list")
    #     # Call the mixin's get_queryset method
    #     self.get_queryset()
        
    #     response = super().list(request, *args, **kwargs)
    #     return response
    
class OrdersRetriveUpdatedeleteView(PlatformApiMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
