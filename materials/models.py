from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Supplier(models.Model):
    """Supplier model for building materials"""

    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'suppliers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Material(models.Model):
    """Material model for building materials"""

    CATEGORY_CHOICES = [
        ('structural', 'Structural Materials'),
        ('finishing', 'Finishing Materials'),
        ('electrical', 'Electrical Supplies'),
        ('plumbing', 'Plumbing Supplies'),
        ('roofing', 'Roofing Materials'),
        ('flooring', 'Flooring Materials'),
        ('paint', 'Paint & Coatings'),
        ('hardware', 'Hardware'),
        ('other', 'Other'),
    ]

    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('bag', 'Bag'),
        ('ton', 'Ton'),
        ('sqm', 'Square Meter'),
        ('sqft', 'Square Foot'),
        ('piece', 'Piece'),
        ('liter', 'Liter'),
        ('gallon', 'Gallon'),
        ('meter', 'Meter'),
        ('foot', 'Foot'),
        ('bundle', 'Bundle'),
        ('box', 'Box'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'materials'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"

    @property
    def current_price(self):
        """Get the most recent price for this material"""
        latest_price = self.prices.order_by('-recorded_at').first()
        return latest_price.price if latest_price else None

    @property
    def average_price(self):
        """Get average price from all suppliers"""
        from django.db.models import Avg
        result = self.prices.aggregate(avg_price=Avg('price'))
        return result['avg_price']


class MaterialPrice(models.Model):
    """Time-series price data for materials"""

    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('api', 'API Integration'),
        ('scraper', 'Web Scraper'),
    ]

    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='prices')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='material_prices')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, default='USD')
    region = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'material_prices'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['material', '-recorded_at']),
            models.Index(fields=['recorded_at']),
        ]

    def __str__(self):
        return f"{self.material.name} - {self.price} {self.currency} ({self.recorded_at.date()})"


class PriceAlert(models.Model):
    """Price alerts for materials"""

    ALERT_TYPE_CHOICES = [
        ('above', 'Price Above Threshold'),
        ('below', 'Price Below Threshold'),
        ('change', 'Price Change Percentage'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='price_alerts')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Alert for {self.material.name} - {self.get_alert_type_display()}"
