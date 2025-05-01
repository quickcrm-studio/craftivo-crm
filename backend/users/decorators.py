from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from functools import wraps
from django.urls import reverse

def group_required(group_names):
    """
    Decorator that checks if a user belongs to at least one of the specified groups.
    Usage: @group_required(['Administrators', 'Managers'])
    """
    def in_groups(user):
        if user.is_superuser:
            return True
        if isinstance(group_names, str):
            groups = [group_names]
        else:
            groups = group_names
        return user.groups.filter(name__in=groups).exists()
    
    return user_passes_test(in_groups, login_url='users:login')

def permission_required(perm):
    """
    Decorator that checks if a user has a specific permission.
    Usage: @permission_required('app.view_model')
    """
    def check_perms(user):
        if user.is_superuser:
            return True
        if isinstance(perm, str):
            perms = (perm, )
        else:
            perms = perm
        return user.has_perms(perms)
    
    return user_passes_test(check_perms, login_url='users:login')

def role_required(view_func=None, redirect_url=None, roles=None):
    """
    Decorator that restricts access to views based on user roles.
    Shows a message and redirects unauthorized users.
    
    Usage: 
    @role_required(roles=['Administrators', 'Managers'])
    def my_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Allow access if user is admin
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            # Check if user is in any of the required roles
            if request.user.groups.filter(name__in=roles).exists():
                return view_func(request, *args, **kwargs)
                
            # User doesn't have access - add message and redirect
            messages.error(
                request, 
                "You don't have permission to access this page. "
                "Please contact an administrator if you need access."
            )
            
            # Redirect to specified URL or home
            if redirect_url:
                return redirect(redirect_url)
            return redirect('home')
            
        return _wrapped_view
    
    # If called with @role_required
    if view_func:
        return decorator(view_func)
    
    # If called with @role_required(roles=[...])
    return decorator 