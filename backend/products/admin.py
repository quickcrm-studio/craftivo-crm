from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductVariation

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ('name', 'description')
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'display_order')

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    fields = ('name', 'value', 'sku_suffix', 'price_adjustment', 'stock_quantity', 'image')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'stock_quantity', 'status', 'image_preview')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('status', 'price', 'stock_quantity')
    readonly_fields = ('created_at', 'updated_at', 'image_preview_large')
    inlines = [ProductImageInline, ProductVariationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'description', 'category', 'status')
        }),
        ('Pricing', {
            'fields': ('price', 'cost')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'reorder_threshold')
        }),
        ('Images', {
            'fields': ('featured_image', 'image_preview_large')
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'length', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.featured_image.url)
        return "No image"
    
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="300" style="max-height: 300px; object-fit: contain;" />', obj.featured_image.url)
        return "No image"
    
    image_preview_large.short_description = 'Image Preview'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductVariation)
