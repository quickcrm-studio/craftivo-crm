from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'customers'

# API Routing
router = DefaultRouter()
router.register(r'api', views.CustomerViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/search/', views.search_customers, name='search_customers'),
    
    # Web UI endpoints
    path('', views.customer_list, name='list'),  # Default list view at the root
    path('list/', views.customer_list, name='list'),
    path('detail/<int:pk>/', views.customer_detail, name='detail'),
    path('create/', views.customer_create, name='create'),
    path('edit/<int:pk>/', views.customer_edit, name='edit'),
    path('delete/<int:pk>/', views.customer_delete, name='delete'),
] 