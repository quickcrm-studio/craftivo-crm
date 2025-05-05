from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q

from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer, CustomerSummarySerializer
from .forms import CustomerForm
from users.decorators import permission_required

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing customers.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'accepts_marketing', 'preferred_communication']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'notes']
    ordering_fields = ['first_name', 'last_name', 'email', 'date_joined', 'status']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerListSerializer
        return CustomerSerializer
    
    def get_permissions(self):
        """
        Return permissions based on action:
        - List/retrieve: Need view_customer permission
        - Create/update/partial_update: Need change_customer permission
        - Destroy: Need delete_customer permission
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

@login_required
def customer_list(request):
    """
    Display a list of customers with pagination.
    """
    search_term = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    customers = Customer.objects.all()
    
    # Apply filters
    if status:
        customers = customers.filter(status=status)
    
    # Apply search if provided
    if search_term:
        customers = customers.filter(
            models.Q(first_name__icontains=search_term) | 
            models.Q(last_name__icontains=search_term) | 
            models.Q(email__icontains=search_term) | 
            models.Q(phone__icontains=search_term)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = 10
    paginator = Paginator(customers, items_per_page)
    
    try:
        customers_page = paginator.page(page)
    except PageNotAnInteger:
        customers_page = paginator.page(1)
    except EmptyPage:
        customers_page = paginator.page(paginator.num_pages)
    
    context = {
        'customers': customers_page,
        'search_term': search_term,
        'selected_status': status,
        'status_choices': Customer.CUSTOMER_STATUS_CHOICES,
        'page_obj': customers_page,
        'is_paginated': True,
        'paginator': paginator
    }
    return render(request, 'customers/customer_list.html', context)

@login_required
def customer_detail(request, pk):
    """
    Display details of a specific customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    context = {'customer': customer}
    return render(request, 'customers/customer_detail.html', context)

@login_required
def customer_create(request):
    """
    Create a new customer.
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer.get_full_name()}" was created successfully.')
            return redirect('customers:detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'submit_text': 'Create Customer'
    }
    return render(request, 'customers/customer_form.html', context)

@login_required
def customer_edit(request, pk):
    """
    Edit an existing customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            updated_customer = form.save()
            messages.success(request, f'Customer "{updated_customer.get_full_name()}" was updated successfully.')
            return redirect('customers:detail', pk=updated_customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
        'submit_text': 'Update Customer'
    }
    return render(request, 'customers/customer_form.html', context)

@login_required
def customer_delete(request, pk):
    """
    Delete a customer.
    """
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'Customer "{customer.get_full_name()}" was deleted successfully.')
        return redirect('customers:list')
    
    context = {'customer': customer}
    return render(request, 'customers/customer_confirm_delete.html', context)

def search_customers(request):
    """
    API endpoint to search for customers.
    Used by the order form to find existing customers.
    """
    search_term = request.GET.get('q', '').strip()
    
    if len(search_term) < 2:
        return JsonResponse({'results': []})
    
    customers = Customer.objects.filter(
        Q(first_name__icontains=search_term) | 
        Q(last_name__icontains=search_term) | 
        Q(email__icontains=search_term) |
        Q(phone__icontains=search_term)
    ).order_by('first_name', 'last_name')[:10]  # Limit to 10 results
    
    results = []
    for customer in customers:
        results.append({
            'id': customer.id,
            'name': customer.get_full_name(),
            'email': customer.email,
            'phone': customer.phone,
            'status': customer.get_status_display(),
            # Include shipping address for auto-population
            'shipping_address': customer.shipping_address,
            'billing_address': customer.billing_address,
        })
    
    return JsonResponse({'results': results})
