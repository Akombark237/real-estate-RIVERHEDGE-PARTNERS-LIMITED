from django.urls import path
from .views import (
    CostEstimateListCreateView,
    CostEstimateDetailView,
    EstimateItemListCreateView,
    EstimateItemDetailView,
    ProjectTemplateListView,
    calculate_estimate
)

urlpatterns = [
    # Cost Estimates
    path('', CostEstimateListCreateView.as_view(), name='estimate-list-create'),
    path('<int:pk>/', CostEstimateDetailView.as_view(), name='estimate-detail'),
    path('calculate/', calculate_estimate, name='calculate-estimate'),
    
    # Estimate Items
    path('<int:estimate_id>/items/', EstimateItemListCreateView.as_view(), name='estimate-item-list-create'),
    path('items/<int:pk>/', EstimateItemDetailView.as_view(), name='estimate-item-detail'),
    
    # Project Templates
    path('templates/', ProjectTemplateListView.as_view(), name='project-template-list'),
]

