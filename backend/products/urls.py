from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'products'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web UI endpoints - Products
    path('', views.product_list, name='list'),  # Default list view at the root
    path('list/', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('detail/<int:pk>/', views.product_detail, name='detail'),
    path('update/<int:pk>/', views.product_update, name='update'),
    path('delete/<int:pk>/', views.product_delete, name='delete'),
    
    # Web UI endpoints - Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
] 