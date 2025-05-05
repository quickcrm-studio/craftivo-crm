from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer
from .serializers import CustomerSerializer, CustomerDetailSerializer
from orders.models import Order
from orders.serializers import OrderSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for customers that allows customers to be viewed, created, edited, and deleted.
    
    This viewset supports versioning through the URL path (e.g., /api/v1/customers/).
    """
    queryset = Customer.objects.all().order_by('last_name', 'first_name')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'state', 'active']
    search_fields = ['first_name', 'last_name', 'email', 'company_name', 'city', 'state']
    ordering_fields = ['first_name', 'last_name', 'email', 'date_joined', 'last_order_date']
    
    def get_serializer_class(self):
        # Check API version
        api_version = self.request.version if hasattr(self.request, 'version') else 'v1'
        
        # For now we only have v1, but this structure allows for future versions
        if api_version == 'v1':
            if self.action == 'retrieve':
                return CustomerDetailSerializer
            return CustomerSerializer
            
        # Default to v1 serializer if version not recognized
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """
        Get all orders for a specific customer.
        """
        customer = self.get_object()
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data) 