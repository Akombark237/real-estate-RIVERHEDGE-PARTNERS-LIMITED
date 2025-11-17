from django.urls import path
from .views import (
    PropertyListCreateView,
    PropertyDetailView,
    PropertyImageListCreateView,
    PropertyImageDetailView,
    PropertyDocumentListCreateView,
    PropertyDocumentDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    my_properties,
    my_transactions
)

urlpatterns = [
    # Properties
    path('', PropertyListCreateView.as_view(), name='property-list-create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('my-properties/', my_properties, name='my-properties'),
    
    # Property Images
    path('<int:property_id>/images/', PropertyImageListCreateView.as_view(), name='property-image-list-create'),
    path('images/<int:pk>/', PropertyImageDetailView.as_view(), name='property-image-detail'),
    
    # Property Documents
    path('<int:property_id>/documents/', PropertyDocumentListCreateView.as_view(), name='property-document-list-create'),
    path('documents/<int:pk>/', PropertyDocumentDetailView.as_view(), name='property-document-detail'),
    
    # Transactions
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('my-transactions/', my_transactions, name='my-transactions'),
]

