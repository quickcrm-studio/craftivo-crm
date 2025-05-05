from rest_framework import serializers
from django.db.models import Count, Sum
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model - basic information.
    """
    full_name = serializers.SerializerMethodField()
    orders_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 
            'company_name', 'city', 'state', 'active', 'date_joined', 
            'last_order_date', 'orders_count'
        ]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_orders_count(self, obj):
        return obj.order_set.count()

class CustomerDetailSerializer(CustomerSerializer):
    """
    Detailed serializer for Customer model with additional information.
    """
    total_spent = serializers.SerializerMethodField()
    avg_order_value = serializers.SerializerMethodField()
    
    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields + [
            'address_line_1', 'address_line_2', 'postal_code', 'country',
            'notes', 'total_spent', 'avg_order_value'
        ]
    
    def get_total_spent(self, obj):
        total = obj.order_set.aggregate(total=Sum('total_amount'))['total']
        return total if total is not None else 0
    
    def get_avg_order_value(self, obj):
        orders_count = obj.order_set.count()
        if orders_count > 0:
            total_spent = self.get_total_spent(obj)
            return round(total_spent / orders_count, 2)
        return 0

class CustomerListSerializer(serializers.ModelSerializer):
    """
    Simplified Customer serializer for list views.
    """
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'status', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class CustomerSummarySerializer(serializers.ModelSerializer):
    """
    Minimal Customer serializer for summary views.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'full_name', 'email', 'status')
        read_only_fields = ('id',)
        
    def get_full_name(self, obj):
        return obj.get_full_name() 