from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsDeliveryCrew
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import ManagerSerializer, DeliveryCrewSerializer, CategorySerializer, \
	MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer



######################
# USER & TOKEN VIEWS #
######################

# POST /auth/users
# GET /auth/users/me
# POST /auth/token/login
# These endpoints have been provided by Djoser. For more info about how to interact with them, 
# review the Postman Workspace




###############################
# USER GROUP MANAGEMENT VIEWS #
###############################

# Base View
class GroupView(ListAPIView, CreateAPIView, DestroyAPIView):
  group_name = None
  queryset = None
  serializer_class = None
  throttle_classes = None
  permission_classes = None

  def __init__(self, group_name, serializer_class, throttle_classes, permission_classes):
    self.group_name = group_name
    self.queryset = User.objects.filter(groups__name = self.group_name)
    self.serializer_class = serializer_class
    self.throttle_classes = throttle_classes
    self.permission_classes = permission_classes

  def post(self, request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username = username)
        group_objects = Group.objects.get(name = self.group_name)
        group_objects.user_set.add(user)
        return Response(
            { 'message': f'The user has been added to the {self.group_name} group' }, 
            HTTP_201_CREATED
        )
    else:
        return Response({'message': 'The username must be provided'}, HTTP_400_BAD_REQUEST)
    
  def delete(self, request, username):
      if username:
        user = get_object_or_404(User, username = username)
        group_objects = Group.objects.get(name = self.group_name)
        group_objects.user_set.remove(user)
        return Response(
            { 'message': f'The user has been removed to the {self.group_name} group' }, 
            HTTP_200_OK
        )
      else:
          return Response({'message': 'The username must be provided'}, HTTP_400_BAD_REQUEST)

# Manager Specific View
class ManagerView(GroupView):
    def __init__(self):
        super().__init__(
            group_name = 'Manager',
            serializer_class = ManagerSerializer,
            throttle_classes = [ AnonRateThrottle, UserRateThrottle ],
            permission_classes = [ IsAdminUser | IsManager ]
        )

# Delivery Crew Specific View
class DeliveryCrewView(GroupView):
    def __init__(self):
        super().__init__(
            group_name = 'DeliveryCrew',
            serializer_class = DeliveryCrewSerializer,
            throttle_classes = [ AnonRateThrottle, UserRateThrottle ],
            permission_classes = [ IsAdminUser | IsManager ]
        )




##################
# CATEGORY VIEWS #
##################
class CategoryView(ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	throttle_classes = [ AnonRateThrottle, UserRateThrottle ]
	permission_classes = [ IsAdminUser ]





####################
# MENU ITEMS VIEWS #
####################

# ...





###############################
# USER GROUP MANAGEMENT VIEWS #
###############################

# ...




#########################
# CART MANAGEMENT VIEWS #
#########################

# ...



##########################
# ORDER MANAGEMENT VIEWS #
##########################

# ...