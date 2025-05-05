from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product, Category
from customers.models import Customer
from orders.models import Order
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """API endpoint that returns dashboard data for the frontend."""
    try:
        # Get current month data
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get basic statistics
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_orders = Order.objects.count()
        total_customers = Customer.objects.count()
        
        # Get pending orders
        pending_orders = Order.objects.exclude(
            status__in=[Order.DELIVERED, Order.SHIPPED, Order.CANCELLED]
        ).count()
        
        # Get revenue for current month
        revenue_this_month = Order.objects.filter(
            created_at__gte=first_day_of_month
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get new customers this month
        new_customers_this_month = Customer.objects.filter(
            date_joined__gte=first_day_of_month
        ).count()
        
        # Get low stock products
        low_stock_products = []
        for product in Product.objects.filter(
            stock_quantity__lt=10, 
            stock_quantity__gt=0
        ).order_by('stock_quantity')[:5]:
            low_stock_products.append({
                'id': product.id,
                'name': product.name,
                'stock': product.stock_quantity,
                'sku': product.sku
            })
        
        # Get out of stock products
        out_of_stock_products = []
        for product in Product.objects.filter(
            stock_quantity=0
        ).order_by('name')[:5]:
            out_of_stock_products.append({
                'id': product.id,
                'name': product.name,
                'sku': product.sku
            })
        
        # Get recent orders
        recent_orders = []
        for order in Order.objects.order_by('-created_at')[:5]:
            recent_orders.append({
                'id': order.id,
                'order_number': order.order_number,
                'customer_name': order.get_customer_name(),
                'total': float(order.total_amount),
                'status': order.get_status_display(),
                'date': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Return complete dashboard data
        return Response({
            'totalProducts': total_products,
            'totalCategories': total_categories,
            'totalOrders': total_orders,
            'totalCustomers': total_customers,
            'pendingOrders': pending_orders,
            'revenueThisMonth': float(revenue_this_month),
            'newCustomersThisMonth': new_customers_this_month,
            'lowStockProducts': low_stock_products,
            'outOfStockProducts': out_of_stock_products,
            'recentOrders': recent_orders
        })
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        return Response({
            'error': 'An error occurred while fetching dashboard data'
        }, status=500) 