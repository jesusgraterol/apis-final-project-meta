from django.contrib.admin import site
from .models import Category, MenuItem, Cart, Order, OrderItem

# Register the Models so they can be used in the Admin GUI
site.register(Category)
site.register(MenuItem)
site.register(Cart)
site.register(Order)
site.register(OrderItem)