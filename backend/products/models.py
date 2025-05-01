from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.conf import settings
import os
import uuid

def product_image_path(instance, filename):
    """
    Generate a unique path for product images.
    Format: products/images/{product_id}/{uuid}-{filename}
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a unique filename with uuid
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    # Return the path
    return os.path.join('products', 'images', str(instance.product.id), unique_filename)

class Category(models.Model):
    """
    Model representing a product category.
    """
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='children', verbose_name=_("Parent Category"))
    
    # Metadata
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Model representing a handmade product in the store.
    """
    # Basic Info
    name = models.CharField(_("Product Name"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True)
    sku = models.CharField(_("SKU"), max_length=50, unique=True)
    description = models.TextField(_("Description"))
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                               related_name='products', verbose_name=_("Category"))
    
    # Pricing
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    cost = models.DecimalField(_("Cost"), max_digits=10, decimal_places=2, 
                             help_text=_("Cost to produce this item"))
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(_("Stock Quantity"), default=0)
    reorder_threshold = models.PositiveIntegerField(_("Reorder Threshold"), default=5,
                                                 help_text=_("Quantity at which to reorder"))
    
    # Status
    DRAFT = 'draft'
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (DRAFT, _('Draft')),
        (ACTIVE, _('Active')),
        (ARCHIVED, _('Archived')),
    ]
    
    status = models.CharField(_("Product Status"), max_length=10, 
                            choices=STATUS_CHOICES, default=DRAFT)
    
    # Physical attributes
    weight = models.DecimalField(_("Weight (g)"), max_digits=7, decimal_places=2, 
                               blank=True, null=True)
    length = models.DecimalField(_("Length (cm)"), max_digits=7, decimal_places=2, 
                               blank=True, null=True)
    width = models.DecimalField(_("Width (cm)"), max_digits=7, decimal_places=2, 
                              blank=True, null=True)
    height = models.DecimalField(_("Height (cm)"), max_digits=7, decimal_places=2, 
                               blank=True, null=True)
    
    # Featured image
    featured_image = models.ImageField(_("Featured Image"), 
                                     upload_to='products/featured/',
                                     blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        """Check if the product is in stock."""
        return self.stock_quantity > 0
    
    @property
    def needs_reordering(self):
        """Check if the product needs to be reordered."""
        return self.stock_quantity < 10
    
    @property
    def primary_image(self):
        """Get the primary image for this product."""
        if self.featured_image:
            return self.featured_image.url
        elif self.images.exists():
            return self.images.first().image.url
        return settings.STATIC_URL + 'products/images/placeholder.png'
    
    @property
    def has_multiple_images(self):
        """Check if the product has multiple images."""
        return self.images.count() > 0 or self.featured_image


class ProductImage(models.Model):
    """
    Model for additional product images.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                              related_name='images', verbose_name=_("Product"))
    image = models.ImageField(_("Image"), upload_to=product_image_path)
    alt_text = models.CharField(_("Alternative Text"), max_length=255, blank=True,
                              help_text=_("Accessibility text for screen readers"))
    display_order = models.PositiveSmallIntegerField(_("Display Order"), default=0,
                                                  help_text=_("Order to display images"))
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['display_order', 'id']
    
    def __str__(self):
        return f"Image for {self.product.name} ({self.id})"


class ProductVariation(models.Model):
    """
    Model for product variations like sizes, colors, etc.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                              related_name='variations', verbose_name=_("Product"))
    name = models.CharField(_("Variation Name"), max_length=100,
                          help_text=_("E.g., Size, Color, Material"))
    value = models.CharField(_("Variation Value"), max_length=100,
                           help_text=_("E.g., Large, Red, Cotton"))
    sku_suffix = models.CharField(_("SKU Suffix"), max_length=20, blank=True,
                               help_text=_("Will be appended to product SKU"))
    price_adjustment = models.DecimalField(_("Price Adjustment"), max_digits=10, decimal_places=2,
                                        default=0, help_text=_("Amount to add/subtract from base price"))
    stock_quantity = models.PositiveIntegerField(_("Stock Quantity"), default=0)
    image = models.ImageField(_("Variation Image"), upload_to=product_image_path, 
                           blank=True, null=True)
    
    class Meta:
        verbose_name = _("Product Variation")
        verbose_name_plural = _("Product Variations")
        unique_together = [['product', 'name', 'value']]
        ordering = ['product', 'name', 'value']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
    
    @property
    def full_sku(self):
        """Return the complete SKU for this variation."""
        if self.sku_suffix:
            return f"{self.product.sku}-{self.sku_suffix}"
        return self.product.sku
    
    @property
    def final_price(self):
        """Calculate the final price for this variation."""
        return self.product.price + self.price_adjustment
