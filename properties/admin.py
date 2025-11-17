from django.contrib import admin
from .models import Property, PropertyImage, PropertyDocument, Transaction


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'city', 'state', 'price', 'status', 'agent', 'listing_date']
    list_filter = ['property_type', 'status', 'city', 'state', 'listing_date']
    search_fields = ['title', 'address', 'city', 'description']
    inlines = [PropertyImageInline, PropertyDocumentInline]
    date_hierarchy = 'listing_date'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['property', 'buyer', 'seller', 'agent', 'sale_price', 'commission_amount', 'status', 'transaction_date']
    list_filter = ['status', 'transaction_date']
    search_fields = ['property__title', 'buyer__email', 'seller__email']
    date_hierarchy = 'transaction_date'
