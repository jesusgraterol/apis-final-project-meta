from django.urls import path
from .views import CategoryView

urlpatterns = [
  # User & Token Endpoints
	# These endpoints are exposed through the /auth routes

  # Category Endpoints
  path('category', CategoryView.as_view()),
  path('category/<int:pk>', CategoryView.as_view())

  # Menu Items Endpoints
  # ...

  # User Group Management Endpoints
  # ...

  # Cart Management Endpoints
  # ...

  # Order Management Endpoints
  # ...
]