from rest_framework.permissions import BasePermission

# IsManager Permission
# Checks if a user is in the 'Manager' group
class IsManager(BasePermission):
  def has_permission(self, request, view):
    return request.user.group.filter(name = 'Manager').exists()
  


# IsDeliveryCrew Permission
# Checks if a user is in the 'DeliveryCrew' group
class IsDeliveryCrew(BasePermission):
  def has_permission(self, request, view):
    return request.user.group.filter(name = 'DeliveryCrew').exists()