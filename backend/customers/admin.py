from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'status', 'date_joined')
    list_filter = ('status', 'accepts_marketing', 'preferred_communication', 'date_joined')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'notes')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Customer Details', {
            'fields': ('status', 'notes')
        }),
        ('Preferences', {
            'fields': ('accepts_marketing', 'preferred_communication')
        }),
    )
    readonly_fields = ('date_joined',)
    date_hierarchy = 'date_joined'
