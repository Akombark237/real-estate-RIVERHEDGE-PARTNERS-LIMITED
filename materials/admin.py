from django.contrib import admin
from .models import Supplier, Material, MaterialPrice, PriceAlert


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'region', 'rating', 'created_at']
    list_filter = ['region', 'created_at']
    search_fields = ['name', 'city', 'contact_person']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'is_active', 'current_price']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(MaterialPrice)
class MaterialPriceAdmin(admin.ModelAdmin):
    list_display = ['material', 'price', 'currency', 'supplier', 'region', 'source', 'recorded_at']
    list_filter = ['source', 'currency', 'recorded_at']
    search_fields = ['material__name', 'supplier__name']
    date_hierarchy = 'recorded_at'


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'material', 'alert_type', 'threshold_value', 'is_active', 'last_triggered']
    list_filter = ['alert_type', 'is_active', 'created_at']
    search_fields = ['user__email', 'material__name']
