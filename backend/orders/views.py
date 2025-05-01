from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect

from .models import Order, OrderItem, OrderStatus
from .forms import OrderForm, OrderItemFormSet, OrderStatusForm
from customers.models import Customer
from products.models import Product, ProductVariation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Order.objects.all()
        
        # Handle search
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(order_number__icontains=search_term) |
                Q(customer__first_name__icontains=search_term) |
                Q(customer__last_name__icontains=search_term) |
                Q(customer__email__icontains=search_term) |
                Q(shipping_name__icontains=search_term)
            )
        
        # Handle status filter
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        # Handle payment status filter
        payment_status = self.request.GET.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_payment_status'] = self.request.GET.get('payment_status', '')
        context['status_choices'] = Order.ORDER_STATUS_CHOICES
        context['payment_status_choices'] = Order.PAYMENT_STATUS_CHOICES
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = order.items.all()
        context['status_history'] = order.status_history.all().order_by('-created_at')
        return context

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = OrderItemFormSet(self.request.POST, prefix='items')
        else:
            context['items_formset'] = OrderItemFormSet(prefix='items')
            
        # For pre-populating from customer if specified via URL
        customer_id = self.request.GET.get('customer')
        if customer_id and not self.request.POST:
            try:
                customer = Customer.objects.get(id=customer_id)
                # Set the customer ID in the form
                context['form'].initial['customer'] = customer.id
                
                # Pre-populate shipping/billing info
                initial = {
                    'shipping_name': f"{customer.first_name} {customer.last_name}",
                    'shipping_address': customer.shipping_address,
                    'shipping_phone': customer.phone,
                    'billing_name': f"{customer.first_name} {customer.last_name}",
                    'billing_address': customer.billing_address,
                }
                
                # Parse address components if available
                if ',' in customer.shipping_address:
                    parts = customer.shipping_address.split(',')
                    if len(parts) > 1:
                        initial['shipping_city'] = parts[1].strip()
                    if len(parts) > 2:
                        state_zip = parts[2].strip().split(' ', 1)
                        if len(state_zip) > 0:
                            initial['shipping_state'] = state_zip[0].strip()
                        if len(state_zip) > 1:
                            initial['shipping_postal_code'] = state_zip[1].strip()
                
                # Do the same for billing if different
                if ',' in customer.billing_address:
                    parts = customer.billing_address.split(',')
                    if len(parts) > 1:
                        initial['billing_city'] = parts[1].strip()
                    if len(parts) > 2:
                        state_zip = parts[2].strip().split(' ', 1)
                        if len(state_zip) > 0:
                            initial['billing_state'] = state_zip[0].strip()
                        if len(state_zip) > 1:
                            initial['billing_postal_code'] = state_zip[1].strip()
                
                initial['shipping_country'] = 'USA'
                initial['billing_country'] = 'USA'
                
                # Update the form's initial data
                context['form'].initial.update(initial)
            except Customer.DoesNotExist:
                pass
                
        # Only include active products
        context['products'] = Product.objects.filter(status=Product.ACTIVE).order_by('name')
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            # Generate order number if not provided
            if not form.instance.order_number:
                import uuid
                form.instance.order_number = uuid.uuid4().hex[:10].upper()
                
            # Save the main order
            self.object = form.save()
            
            # Save the items
            items_formset.instance = self.object
            items_formset.save()
            
            # Create initial status entry
            OrderStatus.objects.create(
                order=self.object,
                status=self.object.status,
                notes="Order created manually",
                created_by=self.request.user.get_full_name() or self.request.user.username
            )
            
            messages.success(self.request, f'Order #{self.object.order_number} has been created successfully.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = OrderItemFormSet(
                self.request.POST, 
                instance=self.object,
                prefix='items'
            )
        else:
            context['items_formset'] = OrderItemFormSet(
                instance=self.object,
                prefix='items'
            )
            
        context['products'] = Product.objects.filter(status=Product.ACTIVE).order_by('name')
        context['status_form'] = OrderStatusForm(initial={'status': self.object.status})
        context['edit_mode'] = True
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            # Check if status changed
            old_status = Order.objects.get(pk=self.object.pk).status
            new_status = form.cleaned_data['status']
            
            # Save the main order
            self.object = form.save()
            
            # Save the items
            items_formset.instance = self.object
            items_formset.save()
            
            # Create status history entry if status changed
            if old_status != new_status:
                OrderStatus.objects.create(
                    order=self.object,
                    status=new_status,
                    notes=f"Status updated from {old_status} to {new_status} during order edit",
                    created_by=self.request.user.get_full_name() or self.request.user.username
                )
                
                # Update timestamps if needed
                if new_status == Order.SHIPPED and not self.object.shipped_at:
                    self.object.shipped_at = timezone.now()
                    self.object.save(update_fields=['shipped_at'])
                elif new_status == Order.DELIVERED and not self.object.delivered_at:
                    self.object.delivered_at = timezone.now()
                    self.object.save(update_fields=['delivered_at'])
            
            messages.success(self.request, f'Order #{self.object.order_number} has been updated successfully.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})

def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status and new_status != order.status:
            # Update order status
            order.status = new_status
            
            # Handle timestamps for specific statuses
            if new_status == Order.SHIPPED:
                order.shipped_at = timezone.now()
            elif new_status == Order.DELIVERED:
                order.delivered_at = timezone.now()
                
            order.save()
            
            # Create status history entry
            OrderStatus.objects.create(
                order=order,
                status=new_status,
                notes=notes,
                created_by=request.user.get_full_name() or request.user.username
            )
            
            messages.success(request, f'Order status updated to {order.get_status_display()}')
        
    return redirect('orders:order_detail', pk=order.pk)
