from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Supplier, Material, MaterialPrice, PriceAlert
from .serializers import (
    SupplierSerializer,
    MaterialSerializer,
    MaterialListSerializer,
    MaterialPriceSerializer,
    PriceAlertSerializer
)


class SupplierListCreateView(generics.ListCreateAPIView):
    """List and create suppliers"""

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'region']
    ordering_fields = ['name', 'rating', 'created_at']


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a supplier"""

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class MaterialListCreateView(generics.ListCreateAPIView):
    """List and create materials"""

    queryset = Material.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MaterialListSerializer
        return MaterialSerializer


class MaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a material"""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]


class MaterialPriceListCreateView(generics.ListCreateAPIView):
    """List and create material prices"""

    serializer_class = MaterialPriceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['material', 'supplier', 'source']
    ordering_fields = ['recorded_at', 'price']

    def get_queryset(self):
        queryset = MaterialPrice.objects.all()
        material_id = self.request.query_params.get('material_id')
        if material_id:
            queryset = queryset.filter(material_id=material_id)
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def material_price_trends(request, material_id):
    """Get price trends for a specific material"""

    try:
        material = Material.objects.get(id=material_id)
    except Material.DoesNotExist:
        return Response({'error': 'Material not found'}, status=status.HTTP_404_NOT_FOUND)

    prices = MaterialPrice.objects.filter(material=material).order_by('-recorded_at')[:30]

    # Calculate statistics
    avg_price = prices.aggregate(avg=Avg('price'))['avg']

    return Response({
        'material': MaterialSerializer(material).data,
        'average_price': avg_price,
        'price_history': MaterialPriceSerializer(prices, many=True).data
    })


class PriceAlertListCreateView(generics.ListCreateAPIView):
    """List and create price alerts"""

    serializer_class = PriceAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PriceAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a price alert"""

    serializer_class = PriceAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)
