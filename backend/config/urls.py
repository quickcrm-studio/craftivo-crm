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
from .api.urls import versioned_router

urlpatterns = [
    # Frontend/UI Routes
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    # App URLs
    path('customers/', include('customers.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    
    # API endpoints - use versioned router
    path('api/', include(versioned_router.get_urls())),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
