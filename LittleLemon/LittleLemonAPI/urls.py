from django.urls import path
from .views import CategoryView, ManagerView, DeliveryCrewView, MenuItemView, CartView, OrderView

urlpatterns = [
  # User & Token Endpoints
	# These endpoints are exposed through the /auth routes

  # Category Endpoints
  path('category', CategoryView.as_view()),
  path('category/<int:pk>', CategoryView.as_view()),

  # User Group Management Endpoints
  path('groups/manager/users', ManagerView.as_view()),
  path('groups/manager/users/<str:username>', ManagerView.as_view()),
  path('groups/delivery-crew/users', DeliveryCrewView.as_view()),
  path('groups/delivery-crew/users/<str:username>', DeliveryCrewView.as_view()),

  # Menu Item Endpoints
  path('menu-items', MenuItemView.as_view()),
  path('menu-items/<int:pk>', MenuItemView.as_view()),

  # Cart Management Endpoints
  path('cart/menu-items', CartView.as_view()),

  # Order Management Endpoints
  path('orders', OrderView.as_view()),
  path('orders/<int:pk>', OrderView.as_view()),
]