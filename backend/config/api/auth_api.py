from django.contrib.auth import logout as django_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from users.models import User
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get the currently logged in user details."""
    try:
        user = request.user
        
        # Create a user data dictionary with basic information
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'permissions': [],
            'groups': []
        }
        
        # Add permissions
        for perm in user.get_all_permissions():
            user_data['permissions'].append(perm)
            
        # Add groups
        for group in user.groups.all():
            user_data['groups'].append(group.name)
            
        return Response(user_data)
    except Exception as e:
        logger.error(f"Error getting current user data: {str(e)}")
        return Response({
            'error': 'An error occurred while fetching user data'
        }, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout the currently logged in user."""
    try:
        # Delete the user's token to logout
        request.auth.delete()
        
        # Also perform Django logout
        django_logout(request)
        
        return Response({'detail': 'Successfully logged out.'})
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return Response({
            'error': 'An error occurred during logout'
        }, status=500) 