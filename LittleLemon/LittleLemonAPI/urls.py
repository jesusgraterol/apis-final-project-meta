from django.urls import path
from .views import CategoryView, ManagerView, DeliveryCrewView

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

  # Menu Items Endpoints
  # ...

  # Cart Management Endpoints
  # ...

  # Order Management Endpoints
  # ...
]