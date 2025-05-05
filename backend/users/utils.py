from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django import forms

def create_groups_with_permissions():
    """
    Create user groups with appropriate permissions.
    This function can be called from a migration or management command.
    """
    # Define group-to-permission mappings with just the available models
    groups_data = {
        'Administrators': {
            'permissions': {
                'auth.group': ['add', 'change', 'delete', 'view'],
                'auth.permission': ['add', 'change', 'delete', 'view'],
                'contenttypes.contenttype': ['add', 'change', 'delete', 'view'],
                'sessions.session': ['add', 'change', 'delete', 'view'],
                'admin.logentry': ['add', 'change', 'delete', 'view'],
            },
            'description': 'Full access to all system features'
        },
        'Managers': {
            'permissions': {
                'auth.group': ['view'],
                'contenttypes.contenttype': ['view'],
                'sessions.session': ['view'],
            },
            'description': 'Can manage business data but limited system access'
        },
        'Sales': {
            'permissions': {
                'auth.group': ['view'],
            },
            'description': 'Can manage orders and customers'
        },
        'Inventory': {
            'permissions': {
                'auth.group': ['view'],
            },
            'description': 'Can manage product inventory'
        },
        'Customer Support': {
            'permissions': {
                'auth.group': ['view'],
            },
            'description': 'Can view customer information'
        }
    }
    
    # Get all available content types 
    all_content_types = {
        f"{ct.app_label}.{ct.model}": ct 
        for ct in ContentType.objects.all()
    }
    
    # Create groups and assign permissions
    for group_name, group_data in groups_data.items():
        group, created = Group.objects.get_or_create(name=group_name)
        
        # Add description as a property if created
        if created:
            print(f"Created group: {group_name}")
        
        # Add permissions for each model
        for app_model_name, actions in group_data['permissions'].items():
            # Skip if the model doesn't exist
            if app_model_name not in all_content_types:
                print(f"Skipping {app_model_name} - content type does not exist")
                continue
                
            content_type = all_content_types[app_model_name]
            model = content_type.model
            
            for action in actions:
                codename = f"{action}_{model}"
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    group.permissions.add(permission)
                    print(f"Added permission {codename} to {group_name}")
                except Permission.DoesNotExist:
                    print(f"Permission {codename} does not exist")

class FormWidgets:
    """
    Common form widgets with consistent styling across the application.
    """
    
    @staticmethod
    def get_text_input(placeholder=None, required=False):
        """
        Return a styled text input widget
        """
        attrs = {
            'class': 'border-gray-300 rounded-md',
        }
        
        if placeholder:
            attrs['placeholder'] = placeholder
            
        if required:
            attrs['required'] = 'required'
            
        return forms.TextInput(attrs=attrs)
    
    @staticmethod
    def get_email_input(placeholder=None, required=False):
        """
        Return a styled email input widget
        """
        attrs = {
            'class': 'border-gray-300 rounded-md',
        }
        
        if placeholder:
            attrs['placeholder'] = placeholder
            
        if required:
            attrs['required'] = 'required'
            
        return forms.EmailInput(attrs=attrs)
    
    @staticmethod
    def get_password_input(placeholder=None, required=False):
        """
        Return a styled password input widget
        """
        attrs = {
            'class': 'border-gray-300 rounded-md',
        }
        
        if placeholder:
            attrs['placeholder'] = placeholder
            
        if required:
            attrs['required'] = 'required'
            
        return forms.PasswordInput(attrs=attrs)
    
    @staticmethod
    def get_textarea(placeholder=None, required=False, rows=3):
        """
        Return a styled textarea widget
        """
        attrs = {
            'class': 'border-gray-300 rounded-md',
            'rows': rows
        }
        
        if placeholder:
            attrs['placeholder'] = placeholder
            
        if required:
            attrs['required'] = 'required'
            
        return forms.Textarea(attrs=attrs)
    
    @staticmethod
    def get_checkbox(required=False):
        """
        Return a styled checkbox widget
        """
        attrs = {
            'class': 'rounded border-gray-300 text-indigo-600'
        }
        
        if required:
            attrs['required'] = 'required'
            
        return forms.CheckboxInput(attrs=attrs)
    
    @staticmethod
    def get_select(required=False):
        """
        Return a styled select widget
        """
        attrs = {
            'class': 'border-gray-300 rounded-md'
        }
        
        if required:
            attrs['required'] = 'required'
            
        return forms.Select(attrs=attrs)
    
    @staticmethod
    def get_checkbox_select_multiple():
        """
        Return a styled checkbox select multiple widget
        """
        attrs = {
            'class': 'rounded border-gray-300 text-indigo-600'
        }
        
        return forms.CheckboxSelectMultiple(attrs=attrs)

# Password validation patterns for reuse
def validate_password_strength(password):
    """
    Validate password meets minimum requirements:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one uppercase letter
    - Contains at least one special character
    """
    from django.core.exceptions import ValidationError
    
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
        
    # Check for digit
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
        
    # Check for uppercase letter
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
        
    # Check for special character
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
    if not any(char in special_characters for char in password):
        raise ValidationError("Password must contain at least one special character.")
        
    return password 