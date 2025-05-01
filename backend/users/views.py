from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import timezone
import datetime

from .forms import UserSignupForm, UserLoginForm, UserEditForm, UserCreateForm, UserProfileForm
from .decorators import role_required
from .models import User

# Create your views here.

def signup(request):
    """
    Allow new staff members to create an account for the CRM.
    """
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = UserSignupForm()
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    """
    Handle user login with rate limiting to prevent brute force attacks.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    # Get client IP address
    ip = request.META.get('REMOTE_ADDR', '')
    
    # Check if this IP is currently blocked
    block_key = f"login_block_{ip}"
    if cache.get(block_key):
        remaining_time = int(cache.ttl(block_key) / 60)
        messages.error(request, f"Too many login attempts. Please try again in {remaining_time} minutes.")
        return render(request, 'users/login.html', {'form': UserLoginForm(), 'blocked': True})
    
    # Check failed login attempts
    attempts_key = f"login_attempts_{ip}"
    attempts = cache.get(attempts_key, 0)
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Reset failed attempts on successful login
                cache.delete(attempts_key)
                
                login(request, user)
                
                # Set session expiry based on remember_me
                if not remember_me:
                    # Session will expire when the user closes their browser
                    request.session.set_expiry(0)
                else:
                    # Session will expire after 2 weeks (1209600 seconds)
                    request.session.set_expiry(1209600)
                
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                
                # Redirect to the page the user was trying to access, or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                # Increment failed login attempts
                attempts += 1
                cache.set(attempts_key, attempts, 300)  # Store for 5 minutes
                
                # Block IP after 5 failed attempts
                if attempts >= 5:
                    # Block for 30 minutes
                    cache.set(block_key, True, 1800)
                    cache.delete(attempts_key)  # Reset attempts counter
                    messages.error(request, "Too many failed login attempts. Your IP has been temporarily blocked for 30 minutes.")
                    return render(request, 'users/login.html', {'form': form, 'blocked': True})
                
                messages.error(request, f"Invalid username or password. You have {5 - attempts} attempts remaining.")
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def profile(request):
    """
    Display and edit user profile information including roles and permissions.
    """
    user = request.user
    groups = user.groups.all()
    permissions = user.get_all_permissions()
    
    # Group permissions by app
    grouped_permissions = {}
    for perm in permissions:
        app, perm_name = perm.split('.', 1)
        if app not in grouped_permissions:
            grouped_permissions[app] = []
        grouped_permissions[app].append(perm_name)
    
    # Handle profile edit form
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            
            # If password was changed, log the user in again
            new_password = form.cleaned_data.get('new_password1')
            if new_password:
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, "Your password has been changed successfully!")
                
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=user, user=user)
    
    context = {
        'user': user,
        'groups': groups,
        'grouped_permissions': grouped_permissions,
        'form': form
    }
    
    return render(request, 'users/profile.html', context)

@role_required(roles=['Administrators'])
def user_management(request):
    """
    Admin view for managing users.
    Only accessible to administrators.
    """
    # Get search term from request
    search_term = request.GET.get('search', '')
    
    # Get all users with optional filtering
    if search_term:
        users = User.objects.filter(
            Q(username__icontains=search_term) | 
            Q(email__icontains=search_term) | 
            Q(first_name__icontains=search_term) | 
            Q(last_name__icontains=search_term)
        ).order_by('username')
    else:
        users = User.objects.all().order_by('username')
    
    # Get all groups for filtering
    groups = Group.objects.all()
    
    # Filter by group if specified
    group_id = request.GET.get('group')
    if group_id:
        users = users.filter(groups__id=group_id)
    
    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = 10
    paginator = Paginator(users, items_per_page)
    
    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)
    
    context = {
        'users': users_page,
        'groups': groups,
        'selected_group': group_id,
        'search_term': search_term,
        'page_obj': users_page,
        'is_paginated': True,
        'paginator': paginator
    }
    
    return render(request, 'users/user_management.html', context)

@role_required(roles=['Administrators'])
def user_create(request):
    """
    Create a new user.
    Only accessible to administrators.
    """
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Add user to selected groups
            if form.cleaned_data.get('groups'):
                for group in form.cleaned_data['groups']:
                    user.groups.add(group)
            
            messages.success(request, f"User '{user.username}' created successfully!")
            return redirect('users:user_management')
    else:
        form = UserCreateForm()
    
    context = {
        'form': form,
        'title': 'Create New User',
        'submit_text': 'Create User'
    }
    
    return render(request, 'users/user_form.html', context)

@role_required(roles=['Administrators'])
def user_edit(request, pk):
    """
    Edit an existing user.
    Only accessible to administrators.
    """
    user = get_object_or_404(User, pk=pk)
    
    # Check if trying to edit a superuser (prevent non-superusers from editing superusers)
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit superusers.")
        return redirect('users:user_management')
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Save the user instance
            updated_user = form.save()
            
            # Update groups
            updated_user.groups.clear()
            for group in form.cleaned_data['groups']:
                updated_user.groups.add(group)
            
            messages.success(request, f"User '{updated_user.username}' updated successfully!")
            return redirect('users:user_management')
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
        'title': f'Edit User: {user.username}',
        'submit_text': 'Update User'
    }
    
    return render(request, 'users/user_form.html', context)

@role_required(roles=['Administrators'])
def user_delete(request, pk):
    """
    Delete a user.
    Only accessible to administrators.
    """
    user = get_object_or_404(User, pk=pk)
    
    # Prevent superusers from being deleted by non-superusers
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete superusers.")
        return redirect('users:user_management')
    
    # Prevent users from deleting themselves
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('users:user_management')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully!")
        return redirect('users:user_management')
    
    context = {
        'user_obj': user
    }
    
    return render(request, 'users/user_confirm_delete.html', context)
