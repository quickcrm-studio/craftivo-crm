from rest_framework import serializers
from .models import Order, OrderItem, OrderStatus
from customers.serializers import CustomerSerializer
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_variation', 'product_name', 
            'sku', 'price', 'quantity', 'line_total', 
            'variation_details', 'product_details'
        ]


class OrderStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = OrderStatus
        fields = [
            'id', 'status', 'status_display', 'notes', 
            'created_by', 'created_at'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusSerializer(many=True, read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'status', 'status_display',
            'total_amount', 'sub_total', 'tax_amount', 'shipping_amount', 
            'discount_amount', 'payment_status', 'payment_status_display',
            'payment_method', 'payment_reference', 'shipping_name', 
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_postal_code', 'shipping_country', 'shipping_phone',
            'billing_name', 'billing_address', 'billing_city', 
            'billing_state', 'billing_postal_code', 'billing_country',
            'customer_notes', 'staff_notes', 'created_at', 'updated_at',
            'shipped_at', 'delivered_at', 'tracking_number', 
            'shipping_carrier', 'items', 'status_history', 'customer_details'
        ] 