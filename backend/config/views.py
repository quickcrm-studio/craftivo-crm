from django.shortcuts import render
from django.db.models import F, Sum, Count
from products.models import Product, Category
from customers.models import Customer
from orders.models import Order
from django.utils import timezone
from datetime import timedelta

def home(request):
    """Home page view with dashboard statistics."""
    # Initialize variables
    low_stock_products = []
    out_of_stock_products = []
    recent_orders = []
    total_orders = 0
    pending_orders = 0
    revenue_this_month = 0
    new_customers_this_month = 0
    
    if request.user.is_authenticated:
        # Get products with stock less than 10 (instead of using reorder_threshold)
        low_stock_products = Product.objects.filter(
            stock_quantity__lt=10,
            stock_quantity__gt=0
        ).order_by('stock_quantity')[:5]
        
        out_of_stock_products = Product.objects.filter(
            stock_quantity=0
        ).order_by('name')[:5]
        
        # Get recent orders
        recent_orders = Order.objects.all().order_by('-created_at')[:5]
        total_orders = Order.objects.count()
        
        # Get pending orders (not delivered, shipped, or cancelled)
        pending_orders = Order.objects.exclude(
            status__in=[Order.DELIVERED, Order.SHIPPED, Order.CANCELLED]
        ).count()
        
        # Get revenue this month
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        revenue_this_month = Order.objects.filter(
            created_at__gte=first_day_of_month
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get new customers this month
        new_customers_this_month = Customer.objects.filter(
            date_joined__gte=first_day_of_month
        ).count()
    
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_orders': total_orders,
        'total_customers': Customer.objects.count(),
        'recent_orders': recent_orders,
        'pending_orders': pending_orders,
        'revenue_this_month': revenue_this_month,
        'new_customers_this_month': new_customers_this_month,
        'is_authenticated': request.user.is_authenticated,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
    }
    return render(request, 'config/home.html', context) 