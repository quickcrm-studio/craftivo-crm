from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Order, OrderItem, OrderStatus
from .serializers import OrderSerializer, OrderItemSerializer, OrderStatusSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['order_number', 'customer__first_name', 'customer__last_name', 'customer__email', 'shipping_name']
    ordering_fields = ['created_at', 'updated_at', 'total_amount']
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending orders."""
        pending_orders = Order.objects.filter(status=Order.PENDING)
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def processing(self, request):
        """Get orders in processing."""
        processing_orders = Order.objects.filter(status=Order.PROCESSING)
        serializer = self.get_serializer(processing_orders, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent orders (last 30 days)."""
        from django.utils import timezone
        import datetime
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago)
        serializer = self.get_serializer(recent_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status with notes."""
        order = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if not new_status or new_status not in dict(Order.ORDER_STATUS_CHOICES):
            return Response(
                {'error': 'Valid status required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update the order status
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Create a status history entry
        OrderStatus.objects.create(
            order=order,
            status=new_status,
            notes=notes,
            created_by=request.user.get_full_name() or request.user.username
        )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data) 