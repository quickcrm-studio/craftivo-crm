from django import forms
from .models import Customer
from users.utils import FormWidgets

class CustomerForm(forms.ModelForm):
    """
    Form for creating and editing customers
    """
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'shipping_address', 'billing_address',
            'status', 'accepts_marketing', 'preferred_communication',
            'notes'
        ]
        widgets = {
            'first_name': FormWidgets.get_text_input(placeholder="First Name"),
            'last_name': FormWidgets.get_text_input(placeholder="Last Name"),
            'email': FormWidgets.get_email_input(placeholder="Email Address"),
            'phone': FormWidgets.get_text_input(placeholder="Phone Number"),
            'shipping_address': FormWidgets.get_textarea(placeholder="Shipping Address", rows=3),
            'billing_address': FormWidgets.get_textarea(placeholder="Billing Address", rows=3),
            'notes': FormWidgets.get_textarea(placeholder="Notes about the customer", rows=3),
            'status': FormWidgets.get_select(),
            'preferred_communication': FormWidgets.get_select(),
            'accepts_marketing': FormWidgets.get_checkbox(),
        } 