from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model with all fields.
    """
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'date_joined')

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