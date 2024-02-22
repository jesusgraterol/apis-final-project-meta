from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsDeliveryCrew
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer,\
OrderItemSerializer

from rest_framework.decorators import api_view


######################
# USER & TOKEN VIEWS #
######################

# POST /auth/users
# GET /auth/users/me
# POST /auth/token/login
# These endpoints have been provided by Djoser. For more info about how to interact with them, 
# review the Postman Workspace





##################
# CATEGORY VIEWS #
##################
class CategoryView(ListAPIView, CreateAPIView, DestroyAPIView):
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