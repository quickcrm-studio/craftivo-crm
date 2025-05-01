from django.contrib import admin
from .models import Order, OrderItem, OrderStatus

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['line_total']
    
class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'payment_status', 
                   'total_amount', 'created_at', 'item_count']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer__first_name', 'customer__last_name', 
                    'customer__email', 'shipping_name', 'tracking_number']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'status')
        }),
        ('Payment Details', {
            'fields': ('sub_total', 'shipping_amount', 'tax_amount', 
                      'discount_amount', 'total_amount', 'payment_status', 
                      'payment_method', 'payment_reference')
        }),
        ('Shipping Information', {
            'fields': ('shipping_name', 'shipping_address', 'shipping_city', 
                      'shipping_state', 'shipping_postal_code', 'shipping_country', 
                      'shipping_phone', 'shipping_carrier', 'tracking_number', 
                      'shipped_at', 'delivered_at')
        }),
        ('Billing Information', {
            'fields': ('billing_name', 'billing_address', 'billing_city', 
                      'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'staff_notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [OrderItemInline, OrderStatusInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_name', 'sku', 'quantity', 'price', 'line_total']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'product_name', 'sku']
    readonly_fields = ['line_total']
    
@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'created_by', 'notes']
    readonly_fields = ['created_at']
