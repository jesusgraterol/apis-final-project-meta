from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view


######################
# USER & TOKEN VIEWS #
######################

# /api/users
# ...
@api_view(['GET', 'POST'])
def users(request):
	return Response('list of books', status = HTTP_200_OK)





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