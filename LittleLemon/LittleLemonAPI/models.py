from django.db.models import Model, SlugField, CharField, DecimalField, BooleanField, \
  SmallIntegerField, DateField, ForeignKey, PROTECT, CASCADE, SET_NULL
from django.contrib.auth.models import User

##################
# CATEGORY MODEL #
##################
class Category(Model):
  slug = SlugField()
  title = CharField(max_length = 255, db_index = True)



###################
# MENU ITEM MODEL #
###################
class MenuItem(Model):
  title = CharField(max_length = 255, db_index = True)
  price = DecimalField(max_digits = 6, decimal_places = 2, db_index = True)
  features = BooleanField(db_index = True)
  category = ForeignKey(Category, on_delete = PROTECT)



##############
# CART MODEL #
##############
class Cart(Model):
  user = ForeignKey(User, on_delete = CASCADE)
  menu_item = ForeignKey(MenuItem, on_delete = CASCADE)
  quantity = SmallIntegerField()
  unit_price = DecimalField(max_digits = 6, decimal_places = 2)
  price = DecimalField(max_digits = 6, decimal_places = 2)

  class Meta:
    unique_together = ('user', 'menu_item')


###############
# ORDER MODEL #
###############
class Order(Model):
  user = ForeignKey(User, on_delete = CASCADE)
  delivery_crew = ForeignKey(User, on_delete = SET_NULL, related_name = 'delivery_crew', null = True)
  status = BooleanField(db_index = True, default = 0)
  total = DecimalField(max_digits = 6, decimal_places = 2)
  date = DateField(db_index = True)



################3###
# ORDER ITEM MODEL #
####################
class OrderItem(Model):
  order = ForeignKey(User, on_delete = CASCADE)
  menu_item = ForeignKey(MenuItem, on_delete = CASCADE)
  quantity = SmallIntegerField()
  unit_price = DecimalField(max_digits = 6, decimal_places = 2)
  price = DecimalField(max_digits = 6, decimal_places = 2)

  class Meta:
    unique_together = ('order', 'menu_item')