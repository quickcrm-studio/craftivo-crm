from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin configuration for the User model."""
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_customer', 'is_vendor')
    list_filter = ('is_staff', 'is_customer', 'is_vendor', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_vendor',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Customer Profile', {'fields': ('company_name', 'address', 'city', 'state', 'zip_code', 'country')}),
        ('Vendor Profile', {'fields': ('business_type', 'tax_id')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_customer', 'is_vendor'),
        }),
    )
