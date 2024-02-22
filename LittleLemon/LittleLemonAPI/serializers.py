from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Category, MenuItem, Cart, Order, OrderItem
from re import match
from django.core.exceptions import ValidationError

#######################
# CATEGORY SERIALIZER #
#######################
class CategorySerializer(ModelSerializer):
  # Validations
  def validate(self, data):
    # validate the slug
    if match('^[a-zA-Z0-9*]{3,100}$', data['slug']) is None:
      raise ValidationError(f'The slug must be a valid string with a length ranging 3 - 100 chars. Received: {data["slug"]}')
    
    # validate the title
    if match('^[a-zA-Z0-9 ]{3,255}$', data['title']) is None:
      raise ValidationError(f'The title must be a valid string with a length ranging 3 - 255 chars. Received: {data["title"]}')

    # return the data if all is well
    return super().validate(data)

  # Metadata
  class Meta:
    model = Category
    fields = [ 'id', 'slug', 'title' ]



########################
# MENU ITEM SERIALIZER #
########################
class MenuItemSerializer(ModelSerializer):
  category_id = IntegerField(write_only=True)

  class Meta:
    model = MenuItem
    fields = [ 'id', 'title', 'price', 'features', 'category', 'category_id' ]



###################
# CART SERIALIZER #
###################
class CartSerializer(ModelSerializer):
  class Meta:
    model = Cart
    fields = [ 'id', 'user', 'menu_item', 'quantity', 'unit_price', 'price' ]



####################
# ORDER SERIALIZER #
####################
class OrderSerializer(ModelSerializer):
  class Meta:
    model = Order
    fields = [ 'id', 'user', 'delivery_crew', 'status', 'total', 'date' ]



#########################
# ORDER ITEM SERIALIZER #
#########################
class OrderItemSerializer(ModelSerializer):
  class Meta:
    model = OrderItem
    fields = [ 'id', 'order', 'menu_item', 'quantity', 'unit_price', 'price' ]

