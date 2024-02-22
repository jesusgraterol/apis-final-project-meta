from functools import reduce
from datetime import date
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, \
  DestroyAPIView
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
  ordering_fields = ['title', 'slug']
  search_fields = ['title', 'slug']
  filterset_fields = ['title', 'slug']

  def get_permissions(self):
    permission_classes = []
    if self.request.method != 'GET':
        permission_classes = [ IsAdminUser | IsManager ]
    return [ permission() for permission in permission_classes ]




###################
# MENU ITEM VIEWS #
###################
class MenuItemView(ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer
  throttle_classes = [ AnonRateThrottle, UserRateThrottle ]
  ordering_fields = [ 'price' ]
  search_fields = [ 'title', 'price', 'featured' ]
  filterset_fields = [ 'category__title' ]

  def get_permissions(self):
    permission_classes = []
    if self.request.method != 'GET':
        permission_classes = [ IsAdminUser | IsManager ]
    return [ permission() for permission in permission_classes ]
  
  def get(self, request):
    # init the items
    items = MenuItem.objects.select_related('category').all()

    # extract the filtering query values
    category_id = request.query_params.get('category_id')
    if category_id:
      items = items.filter(category = category_id)

    # extract the ordering query values (if any)
    order_by = request.query_params.get('order_by')
    if order_by:
       items = items.order_by(order_by)
     
    # init the pagination config (if any)
    page = request.query_params.get('page')
    perpage = request.query_params.get('perpage')
    if page and perpage:
      paginator = Paginator(items, per_page=perpage)
      try:
        items = paginator.page(number=page)
      except EmptyPage:
        items = []

    # finally, serialize the items and return them
    serialized_items = MenuItemSerializer(items, many = True)
    return Response(serialized_items.data, HTTP_200_OK)

  
  def patch(self, request, pk):
     item = get_object_or_404(MenuItem, pk = pk)
     item.featured = not item.featured
     item.save()
     return Response(
        { 'message': f'The menu item {pk} featured state has been toggled to {item.featured}' },
        HTTP_200_OK
     )





#########################
# CART MANAGEMENT VIEWS #
#########################
class CartView(ListAPIView, CreateAPIView):
  serializer_class = CartSerializer
  throttle_classes = [ AnonRateThrottle, UserRateThrottle ]
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
     return Cart.objects.filter(user = self.request.user)
  
  def post(self, request):
     menu_item_id = request.data['menu_item']
     menu_item = get_object_or_404(MenuItem, id = menu_item_id)
     quantity = request.data['quantity']
     price = int(quantity) * menu_item.price
     Cart.objects.create(
        user = request.user,
        menu_item = menu_item,
        quantity = quantity,
        unit_price = menu_item.price,
        price = price
     )
     return Response(
        { 'message': f'The item {menu_item_id} was added to the cart'}, 
        HTTP_201_CREATED
      )

  def delete(self, request):
     Cart.objects.filter(user = request.user).delete()
     return Response(
        { 'message': f'The cart items have been deleted'}, 
        HTTP_200_OK
      )



##########################
# ORDER MANAGEMENT VIEWS #
##########################
class OrderView(ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
  serializer_class = OrderSerializer
  throttle_classes = [ AnonRateThrottle, UserRateThrottle ]

  def get_queryset(self):
     # retrieve all the orders if it is the admin or a manager
     if self.request.user.is_superuser or self.request.user.groups.filter(name = 'Manager').exists():
        return Order.objects.all()
     # if the user belongs to the DeliveryCrew group, only return the orders assigned to him/her
     elif self.request.user.groups.filter(name = 'DeliveryCrew').exists():
        return Order.objects.filter(delivery_crew = self.request.user)
     # otherwise, retrieve the users' own orders
     else:
        return Order.objects.filter(user = self.request.user)
     
  def get_permissions(self):
    permission_classes = []
    # users can send GET and POST requests as long as they are authenticated
    if self.request.method == 'GET' or self.request.method == 'POST':
      permission_classes = [ IsAuthenticated ]
    # the delivery crew can patch the status of the order
    elif self.request.method == 'PATCH':
       permission_classes = [ IsDeliveryCrew ]
    # the manager and the admin can assign an order to a delivery crew user or delete it
    elif self.request.method == 'PUT' or self.request.method == 'DELETE':
       permission_classes = [ IsManager | IsAdminUser ]
    return [ permission() for permission in permission_classes ]
       
  def post(self, request):
    # init the cart model and make sure there are items in it
    cart = Cart.objects.filter(user = request.user)
    cart_items = cart.values()
    if len(cart_items) == 0:
      return Response({'message': 'Cannot place an order for an empty cart'}, HTTP_400_BAD_REQUEST)
    
    # calculate the amount of money the order is worth
    order_total = reduce(lambda x, y: x['price'] + y['price'], cart_items)

    # store the order
    order = Order.objects.create(
       user = request.user, 
       status = False, 
       total = order_total, 
       date = date.today()
    )

    # store each cart item in the order items
    for item in cart_items:
       menu_item = get_object_or_404(MenuItem, id = item['menu_item_id'])
       order_item = OrderItem.objects.create(
          order = order, 
          menu_item = menu_item,
          quantity = item['quantity'],
          unit_price = item['unit_price'],
          price = item['price'],
        )
       order_item.save()

    # clear the cart
    cart.delete()

    # finally, return the result
    return Response({'message': f'The order ID {order.id} has been placed'}, HTTP_201_CREATED)
  
  def patch(self, request, pk):
     order = Order.objects.get(pk = pk)
     order.status = not order.status
     order.save()
     return Response(
        {'message': f'The status of the order ID {order.id} has set to {order.status}'}, 
        HTTP_200_OK
      )
  
  def put(self, request, pk):
     # ensure the crew nickname was provided
     delivery_crew_nickname = request.data['delivery_crew_nickname']
     if not delivery_crew_nickname:
        return Response({'message': 'The delivery_crew_nickname must be provided'}, HTTP_400_BAD_REQUEST)
     
     # retrieve the order and the delivery crew user
     order = get_object_or_404(Order, pk = pk)
     delivery_crew_user = get_object_or_404(User, username = delivery_crew_nickname)

     # assign the order to the user
     order.delivery_crew = delivery_crew_user
     order.save()
     return Response(
        {'message': f'The delivery crew {delivery_crew_nickname} was assigned to the order {pk}'},
        HTTP_200_OK
     )