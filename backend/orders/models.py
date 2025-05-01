from django.db import models
from django.utils.translation import gettext_lazy as _
from customers.models import Customer
from products.models import Product, ProductVariation
import uuid

class Order(models.Model):
    """
    Model representing a customer order.
    """
    # Order number and tracking
    order_number = models.CharField(_("Order Number"), max_length=32, unique=True, 
                                  editable=False, default=uuid.uuid4().hex[:10].upper())
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, 
                                related_name='orders', verbose_name=_("Customer"))
    
    # Order status
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'
    
    ORDER_STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (PROCESSING, _('Processing')),
        (SHIPPED, _('Shipped')),
        (DELIVERED, _('Delivered')),
        (CANCELLED, _('Cancelled')),
        (REFUNDED, _('Refunded')),
    ]
    
    status = models.CharField(_("Order Status"), max_length=20, 
                            choices=ORDER_STATUS_CHOICES, default=PENDING)
    
    # Payment information
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(_("Subtotal"), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_("Tax Amount"), max_digits=10, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(_("Shipping Amount"), max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(_("Discount"), max_digits=10, decimal_places=2, default=0.00)
    
    PAYMENT_PENDING = 'pending'
    PAYMENT_PAID = 'paid'
    PAYMENT_FAILED = 'failed'
    PAYMENT_REFUNDED = 'refunded'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, _('Pending')),
        (PAYMENT_PAID, _('Paid')),
        (PAYMENT_FAILED, _('Failed')),
        (PAYMENT_REFUNDED, _('Refunded')),
    ]
    
    payment_status = models.CharField(_("Payment Status"), max_length=20,
                                    choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    payment_method = models.CharField(_("Payment Method"), max_length=50, blank=True)
    payment_reference = models.CharField(_("Payment Reference"), max_length=100, blank=True)
    
    # Shipping information
    shipping_name = models.CharField(_("Shipping Name"), max_length=100)
    shipping_address = models.TextField(_("Shipping Address"))
    shipping_city = models.CharField(_("City"), max_length=100)
    shipping_state = models.CharField(_("State/Province"), max_length=100)
    shipping_postal_code = models.CharField(_("Postal/Zip Code"), max_length=20)
    shipping_country = models.CharField(_("Country"), max_length=100)
    shipping_phone = models.CharField(_("Phone"), max_length=20)
    
    # Billing information
    billing_name = models.CharField(_("Billing Name"), max_length=100)
    billing_address = models.TextField(_("Billing Address"))
    billing_city = models.CharField(_("City"), max_length=100)
    billing_state = models.CharField(_("State/Province"), max_length=100)
    billing_postal_code = models.CharField(_("Postal/Zip Code"), max_length=20)
    billing_country = models.CharField(_("Country"), max_length=100)
    
    # Notes and metadata
    customer_notes = models.TextField(_("Customer Notes"), blank=True)
    staff_notes = models.TextField(_("Staff Notes"), blank=True)
    
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    shipped_at = models.DateTimeField(_("Shipped At"), null=True, blank=True)
    delivered_at = models.DateTimeField(_("Delivered At"), null=True, blank=True)
    
    tracking_number = models.CharField(_("Tracking Number"), max_length=100, blank=True)
    shipping_carrier = models.CharField(_("Shipping Carrier"), max_length=100, blank=True)
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)
    
    @property
    def is_paid(self):
        """Check if order is paid."""
        return self.payment_status == self.PAYMENT_PAID
    
    @property
    def can_be_cancelled(self):
        """Check if order can be cancelled."""
        return self.status in [self.PENDING, self.PROCESSING]
    
    @property
    def is_completed(self):
        """Check if order is completed."""
        return self.status == self.DELIVERED
    
    @property
    def item_count(self):
        """Get the total number of items in the order."""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                            related_name='items', verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                              related_name='order_items', verbose_name=_("Product"))
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='order_items', 
                                        verbose_name=_("Product Variation"))
    
    # Even if the product is deleted, we keep a record of what was ordered
    product_name = models.CharField(_("Product Name"), max_length=200)
    sku = models.CharField(_("SKU"), max_length=50)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    
    # Calculated fields
    line_total = models.DecimalField(_("Line Total"), max_digits=10, decimal_places=2)
    
    # Optional variation details
    variation_details = models.JSONField(_("Variation Details"), null=True, blank=True,
                                      help_text=_("JSON representation of the variation details"))
    
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    def save(self, *args, **kwargs):
        """
        Calculate line total before saving.
        """
        self.line_total = self.price * self.quantity
        super().save(*args, **kwargs)


class OrderStatus(models.Model):
    """
    Model for tracking order status changes.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                            related_name='status_history', verbose_name=_("Order"))
    status = models.CharField(_("Order Status"), max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    notes = models.TextField(_("Notes"), blank=True)
    created_by = models.CharField(_("Created By"), max_length=100, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Order Status")
        verbose_name_plural = _("Order Status History")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"
