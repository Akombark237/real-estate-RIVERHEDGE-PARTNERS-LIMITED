from django.urls import path
from .views import (
    SupplierListCreateView,
    SupplierDetailView,
    MaterialListCreateView,
    MaterialDetailView,
    MaterialPriceListCreateView,
    material_price_trends,
    PriceAlertListCreateView,
    PriceAlertDetailView
)

urlpatterns = [
    # Suppliers
    path('suppliers/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    
    # Materials
    path('', MaterialListCreateView.as_view(), name='material-list-create'),
    path('<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),
    
    # Material Prices
    path('prices/', MaterialPriceListCreateView.as_view(), name='material-price-list-create'),
    path('<int:material_id>/price-trends/', material_price_trends, name='material-price-trends'),
    
    # Price Alerts
    path('alerts/', PriceAlertListCreateView.as_view(), name='price-alert-list-create'),
    path('alerts/<int:pk>/', PriceAlertDetailView.as_view(), name='price-alert-detail'),
]

