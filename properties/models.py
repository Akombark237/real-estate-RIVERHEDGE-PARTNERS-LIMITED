from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Property(models.Model):
    """Property listing model"""

    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
        ('industrial', 'Industrial'),
        ('mixed', 'Mixed Use'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('off_market', 'Off Market'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)

    # Location
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='USA')
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Pricing
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, default='USD')

    # Property Details
    size_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    parking_spaces = models.IntegerField(default=0)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    listing_date = models.DateField(auto_now_add=True)

    # Relationships
    agent = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='properties')
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_properties')

    # Features
    features = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'properties'
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} - {self.city}, {self.state}"


class PropertyImage(models.Model):
    """Property images"""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_images'
        ordering = ['order', '-is_primary']

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyDocument(models.Model):
    """Property documents (contracts, certificates, etc.)"""

    DOCUMENT_TYPE_CHOICES = [
        ('contract', 'Contract'),
        ('deed', 'Deed'),
        ('certificate', 'Certificate'),
        ('inspection', 'Inspection Report'),
        ('appraisal', 'Appraisal'),
        ('other', 'Other'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='property_documents/')
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.property.title}"


class Transaction(models.Model):
    """Property transaction model"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='purchases')
    seller = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='sales')
    agent = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='transactions')

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'))
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate commission amount
        if self.sale_price and self.commission_rate:
            self.commission_amount = (self.sale_price * self.commission_rate) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction for {self.property.title} - {self.status}"
