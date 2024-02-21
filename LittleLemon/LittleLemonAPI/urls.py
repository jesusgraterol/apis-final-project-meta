from django.urls import path
from .views import users

urlpatterns = [
  # User & Token Endpoints
	path('users/', users),

  # Menu Items Endpoints
  # ...

  # User Group Management Endpoints
  # ...

  # Cart Management Endpoints
  # ...

  # Order Management Endpoints
  # ...
]