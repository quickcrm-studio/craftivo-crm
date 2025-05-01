from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, OrderStatus
from customers.models import Customer
from products.models import Product, ProductVariation
from decimal import Decimal

class OrderForm(forms.ModelForm):
    # Add field for searching existing customers
    customer_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            'placeholder': 'Search by name or email...',
            'autocomplete': 'off',
            'id': 'customer-search'
        }),
        label="Search Existing Customer"
    )
    
    # Add fields for creating a new customer
    customer_first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'First Name'}),
        label="First Name"
    )
    
    customer_last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Last Name'}),
        label="Last Name"
    )
    
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Email'}),
        label="Email"
    )
    
    customer_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Phone Number'}),
        label="Phone"
    )
    
    customer_marketing = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'}),
        label="Subscribe to marketing"
    )
    
    class Meta:
        model = Order
        fields = [
            'customer', 'status', 'payment_status', 'payment_method', 'payment_reference',
            'shipping_name', 'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_postal_code', 'shipping_country', 'shipping_phone',
            'billing_name', 'billing_address', 'billing_city', 'billing_state', 
            'billing_postal_code', 'billing_country',
            'customer_notes', 'staff_notes',
            'shipping_carrier', 'tracking_number',
            'sub_total', 'shipping_amount', 'tax_amount', 'discount_amount', 'total_amount'
        ]
        widgets = {
            'customer': forms.HiddenInput(),  # Make this a hidden field
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'payment_status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'payment_method': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'payment_reference': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            
            'shipping_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'shipping_address': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 2}),
            'shipping_city': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'shipping_state': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'shipping_country': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            
            'billing_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'billing_address': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 2}),
            'billing_city': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'billing_state': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'billing_postal_code': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'billing_country': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            
            'customer_notes': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 3}),
            'staff_notes': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 3}),
            
            'shipping_carrier': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'tracking_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            
            'sub_total': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'readonly': True}),
            'shipping_amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'tax_amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'total_amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'readonly': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default values for new orders
        if not self.instance.pk:
            self.fields['shipping_amount'].initial = Decimal('0.00')
            self.fields['tax_amount'].initial = Decimal('0.00')
            self.fields['discount_amount'].initial = Decimal('0.00')
            self.fields['sub_total'].initial = Decimal('0.00')
            self.fields['total_amount'].initial = Decimal('0.00')
            self.fields['shipping_country'].initial = 'USA'
            self.fields['billing_country'].initial = 'USA'
            
        # Make some fields optional
        self.fields['customer'].required = False
        self.fields['shipping_carrier'].required = False
        self.fields['tracking_number'].required = False
        self.fields['payment_method'].required = False
        self.fields['payment_reference'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if customer is selected or if we need to create a new one
        customer = cleaned_data.get('customer')
        customer_first_name = cleaned_data.get('customer_first_name')
        customer_last_name = cleaned_data.get('customer_last_name')
        customer_email = cleaned_data.get('customer_email')
        
        # Validate that either an existing customer is selected or new customer info is provided
        if not customer and not (customer_first_name and customer_last_name):
            if self.instance.pk:  # If editing existing order, don't require customer
                pass
            else:  # New order requires customer info
                raise forms.ValidationError("Either select an existing customer or provide new customer information")
        
        # For new customers, email is required
        if customer_first_name and customer_last_name and not customer_email:
            raise forms.ValidationError("Email is required for new customers")
            
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if we need to create a new customer
        if not instance.customer_id and self.cleaned_data.get('customer_first_name') and self.cleaned_data.get('customer_last_name'):
            # Create new customer
            customer = Customer(
                first_name=self.cleaned_data['customer_first_name'],
                last_name=self.cleaned_data['customer_last_name'],
                email=self.cleaned_data['customer_email'],
                phone=self.cleaned_data.get('customer_phone', ''),
                shipping_address=instance.shipping_address,
                billing_address=instance.billing_address,
                status=Customer.NEW,
                accepts_marketing=self.cleaned_data.get('customer_marketing', False),
                preferred_communication='email'
            )
            customer.save()
            
            # Link the customer to the order
            instance.customer = customer
        
        if commit:
            instance.save()
        
        return instance

class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(status=Product.ACTIVE),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm product-select'})
    )
    
    product_variation = forms.ModelChoiceField(
        queryset=ProductVariation.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm variation-select'})
    )
    
    class Meta:
        model = OrderItem
        fields = ['product', 'product_variation', 'product_name', 'sku', 'price', 'quantity', 'line_total']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'readonly': True}),
            'sku': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'readonly': True}),
            'price': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'min': '1'}),
            'line_total': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'readonly': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        instance = kwargs.get('instance')
        
        # Set default values
        if instance and instance.product_id:
            self.fields['product_variation'].queryset = ProductVariation.objects.filter(
                product=instance.product
            )

# Create formset for order items
OrderItemFormSet = inlineformset_factory(
    Order, 
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)

class OrderStatusForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 2}),
        required=False
    )
    
    class Meta:
        model = OrderStatus
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
        } 