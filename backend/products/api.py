from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Product, Category, ProductImage, ProductVariation
from .serializers import ProductSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in this category."""
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products that need reordering."""
        products = Product.objects.filter(stock_quantity__lte=models.F('reorder_threshold'))
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get products that are out of stock."""
        products = Product.objects.filter(stock_quantity=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update the stock quantity of a product."""
        product = self.get_object()
        
        try:
            quantity = int(request.data.get('quantity', 0))
        except (ValueError, TypeError):
            return Response(
                {'error': 'Quantity must be a valid integer.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update stock
        product.stock_quantity = max(0, product.stock_quantity + quantity)
        product.save()
        
        serializer = self.get_serializer(product)
        return Response(serializer.data) 