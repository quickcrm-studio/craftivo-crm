from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from customers.api import CustomerViewSet
from products.api import ProductViewSet, CategoryViewSet
from orders.api import OrderViewSet
from config.api import dashboard_api, auth_api
from config.api.docs import api_version_info

# Generate separate routers for each API version
class VersionedRouter:
    def __init__(self):
        self.v1_router = routers.DefaultRouter()
        
        # Register v1 routes
        self.v1_router.register(r'customers', CustomerViewSet)
        self.v1_router.register(r'products', ProductViewSet)
        self.v1_router.register(r'categories', CategoryViewSet)
        self.v1_router.register(r'orders', OrderViewSet)
    
    def get_urls(self):
        return [
            # API version documentation
            path('docs/', api_version_info, name='api_version_info'),
            
            # v1 API endpoints
            path('v1/', include([
                path('', include(self.v1_router.urls)),
                path('dashboard/', dashboard_api.dashboard_data, name='api_v1_dashboard'),
                path('auth/login/', csrf_exempt(obtain_auth_token), name='api_v1_token_auth'),
                path('auth/user/', auth_api.get_current_user, name='api_v1_current_user'),
                path('auth/logout/', auth_api.logout, name='api_v1_logout'),
            ])),
            
            # Browsable API login/logout views
            path('auth/', include('rest_framework.urls', namespace='rest_framework')),
        ]

# Initialize the versioned router
versioned_router = VersionedRouter() 