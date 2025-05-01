from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'customers'

# API Routing
router = DefaultRouter()
router.register(r'api', views.CustomerViewSet)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    path('api/search/', views.search_customers, name='search_customers'),
    
    # Web UI endpoints
    path('list/', views.customer_list, name='customer_list'),
    path('detail/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('create/', views.customer_create, name='customer_create'),
    path('edit/<int:pk>/', views.customer_edit, name='customer_edit'),
] 