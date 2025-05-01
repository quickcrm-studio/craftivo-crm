from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategoryNestedSerializer(serializers.ModelSerializer):
    """Simplified Category serializer for nesting in other serializers."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""
    category = CategoryNestedSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    
    is_in_stock = serializers.BooleanField(read_only=True)
    needs_reordering = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'description', 
            'category', 'category_id', 'price', 'cost',
            'stock_quantity', 'reorder_threshold', 'status',
            'weight', 'length', 'width', 'height',
            'is_in_stock', 'needs_reordering',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 