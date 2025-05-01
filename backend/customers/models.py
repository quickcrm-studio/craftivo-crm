from django.db import models
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    """
    Model representing a customer who buys products from the store.
    """
    # Contact Information
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    email = models.EmailField(_("Email Address"), unique=True)
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    
    # Addresses
    shipping_address = models.TextField(_("Shipping Address"), blank=True)
    billing_address = models.TextField(_("Billing Address"), blank=True)
    
    # Customer Details
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    notes = models.TextField(_("Notes"), blank=True)
    
    # Customer Status
    LEAD = 'lead'
    NEW = 'new'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    FORMER = 'former'
    
    CUSTOMER_STATUS_CHOICES = [
        (LEAD, _('Lead')),
        (NEW, _('New')),
        (ACTIVE, _('Active')),
        (INACTIVE, _('Inactive')),
        (FORMER, _('Former')),
    ]
    
    status = models.CharField(
        _("Customer Status"),
        max_length=10,
        choices=CUSTOMER_STATUS_CHOICES,
        default=NEW,
    )
    
    # Preferences
    accepts_marketing = models.BooleanField(_("Accepts Marketing"), default=False)
    preferred_communication = models.CharField(
        _("Preferred Communication"), 
        max_length=10,
        choices=[('email', _('Email')), ('phone', _('Phone')), ('sms', _('SMS'))],
        default='email',
    )
    
    # Metadata
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """
        Return the customer's full name.
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        """
        Return the customer's first name.
        """
        return self.first_name
    
    @property
    def is_active(self):
        """
        Check if the customer is active.
        """
        return self.status == self.ACTIVE
