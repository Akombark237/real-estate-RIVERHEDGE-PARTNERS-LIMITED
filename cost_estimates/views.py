from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .models import CostEstimate, EstimateItem, ProjectTemplate
from .serializers import (
    CostEstimateSerializer,
    CostEstimateListSerializer,
    EstimateItemSerializer,
    ProjectTemplateSerializer
)


class CostEstimateListCreateView(generics.ListCreateAPIView):
    """List and create cost estimates"""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project_type', 'quality_level', 'status']
    ordering_fields = ['estimate_date', 'total_cost', 'created_at']

    def get_queryset(self):
        return CostEstimate.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CostEstimateListSerializer
        return CostEstimateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CostEstimateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cost estimate"""

    serializer_class = CostEstimateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CostEstimate.objects.filter(user=self.request.user)


class EstimateItemListCreateView(generics.ListCreateAPIView):
    """List and create estimate items"""

    serializer_class = EstimateItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        estimate_id = self.kwargs.get('estimate_id')
        return EstimateItem.objects.filter(estimate_id=estimate_id)

    def perform_create(self, serializer):
        estimate_id = self.kwargs.get('estimate_id')
        serializer.save(estimate_id=estimate_id)


class EstimateItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an estimate item"""

    queryset = EstimateItem.objects.all()
    serializer_class = EstimateItemSerializer
    permission_classes = [IsAuthenticated]


class ProjectTemplateListView(generics.ListAPIView):
    """List project templates"""

    queryset = ProjectTemplate.objects.filter(is_active=True)
    serializer_class = ProjectTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project_type', 'quality_level']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_estimate(request):
    """Calculate cost estimate based on parameters"""

    project_type = request.data.get('project_type')
    quality_level = request.data.get('quality_level', 'standard')
    area_sqft = Decimal(request.data.get('area_sqft', 0))

    # Base cost per sqft based on quality level
    base_costs = {
        'basic': Decimal('80.00'),
        'standard': Decimal('120.00'),
        'premium': Decimal('180.00'),
        'luxury': Decimal('250.00'),
    }

    base_cost_per_sqft = base_costs.get(quality_level, Decimal('120.00'))

    # Calculate costs
    material_cost = area_sqft * base_cost_per_sqft * Decimal('0.60')  # 60% materials
    labor_cost = area_sqft * base_cost_per_sqft * Decimal('0.30')     # 30% labor
    overhead_cost = area_sqft * base_cost_per_sqft * Decimal('0.10')  # 10% overhead
    total_cost = material_cost + labor_cost + overhead_cost

    return Response({
        'area_sqft': area_sqft,
        'quality_level': quality_level,
        'base_cost_per_sqft': base_cost_per_sqft,
        'material_cost': material_cost,
        'labor_cost': labor_cost,
        'overhead_cost': overhead_cost,
        'total_cost': total_cost,
        'currency': 'USD'
    })
