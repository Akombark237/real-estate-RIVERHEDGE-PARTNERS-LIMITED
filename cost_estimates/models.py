from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class CostEstimate(models.Model):
    """Cost estimate for construction or renovation projects"""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('final', 'Final'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('new_construction', 'New Construction'),
        ('renovation', 'Renovation'),
        ('extension', 'Extension'),
        ('repair', 'Repair'),
        ('custom', 'Custom Project'),
    ]

    QUALITY_LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('luxury', 'Luxury'),
    ]

    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPE_CHOICES)
    quality_level = models.CharField(max_length=20, choices=QUALITY_LEVEL_CHOICES, default='standard')

    property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='estimates')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cost_estimates')

    # Project dimensions
    total_area_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_area_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Cost breakdown
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    labor_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    equipment_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    overhead_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    currency = models.CharField(max_length=3, default='USD')

    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    estimate_date = models.DateField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)

    # Additional info
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cost_estimates'
        ordering = ['-created_at']

    def calculate_total(self):
        """Calculate total cost from all items"""
        items_total = sum(item.total_price for item in self.items.all())
        self.material_cost = items_total
        self.total_cost = self.material_cost + self.labor_cost + self.equipment_cost + self.overhead_cost
        return self.total_cost

    def save(self, *args, **kwargs):
        # Recalculate total before saving
        if self.pk:  # Only if already exists
            self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_name} - {self.total_cost} {self.currency}"


class EstimateItem(models.Model):
    """Individual items in a cost estimate"""

    estimate = models.ForeignKey(CostEstimate, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey('materials.Material', on_delete=models.SET_NULL, null=True, blank=True)

    # Item details
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    # Quantity and pricing
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit = models.CharField(max_length=20)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    # Additional costs
    labor_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    labor_rate = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    notes = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'estimate_items'
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        # Auto-calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Update estimate total
        if self.estimate_id:
            self.estimate.calculate_total()
            self.estimate.save()

    def __str__(self):
        return f"{self.item_name} - {self.quantity} {self.unit}"


class ProjectTemplate(models.Model):
    """Pre-defined templates for common construction projects"""

    name = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.CharField(max_length=30, choices=CostEstimate.PROJECT_TYPE_CHOICES)
    quality_level = models.CharField(max_length=20, choices=CostEstimate.QUALITY_LEVEL_CHOICES)

    # Default values
    default_area_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_duration_days = models.IntegerField(null=True, blank=True)

    # Template items (JSON format)
    template_items = models.JSONField(default=list)

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_templates'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_quality_level_display()})"
