"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from .api import dashboard_api, auth_api
from customers.api import CustomerViewSet
from products.api import ProductViewSet, CategoryViewSet
from orders.api import OrderViewSet

# API Router
router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Frontend/UI Routes
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    # App URLs
    path('customers/', include('customers.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/dashboard/', dashboard_api.dashboard_data, name='dashboard_api'),
    path('api/auth/login/', csrf_exempt(obtain_auth_token), name='api_token_auth'),
    path('api/auth/user/', auth_api.get_current_user, name='api_current_user'),
    path('api/auth/logout/', auth_api.logout, name='api_logout'),
    
    # API docs
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
