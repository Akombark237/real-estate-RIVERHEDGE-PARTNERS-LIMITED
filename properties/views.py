from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, PropertyImage, PropertyDocument, Transaction
from .serializers import (
    PropertySerializer,
    PropertyListSerializer,
    PropertyImageSerializer,
    PropertyDocumentSerializer,
    TransactionSerializer
)


class PropertyListCreateView(generics.ListCreateAPIView):
    """List and create properties"""

    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'status', 'city', 'state', 'agent']
    search_fields = ['title', 'description', 'address', 'city']
    ordering_fields = ['price', 'listing_date', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PropertyListSerializer
        return PropertySerializer

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a property"""

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]


class PropertyImageListCreateView(generics.ListCreateAPIView):
    """List and create property images"""

    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return PropertyImage.objects.filter(property_id=property_id)

    def perform_create(self, serializer):
        property_id = self.kwargs.get('property_id')
        serializer.save(property_id=property_id)


class PropertyImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a property image"""

    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]


class PropertyDocumentListCreateView(generics.ListCreateAPIView):
    """List and create property documents"""

    serializer_class = PropertyDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return PropertyDocument.objects.filter(property_id=property_id)

    def perform_create(self, serializer):
        property_id = self.kwargs.get('property_id')
        serializer.save(property_id=property_id, uploaded_by=self.request.user)


class PropertyDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a property document"""

    queryset = PropertyDocument.objects.all()
    serializer_class = PropertyDocumentSerializer
    permission_classes = [IsAuthenticated]


class TransactionListCreateView(generics.ListCreateAPIView):
    """List and create transactions"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'agent', 'buyer', 'seller']
    ordering_fields = ['transaction_date', 'sale_price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a transaction"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_properties(request):
    """Get properties for the current user"""

    properties = Property.objects.filter(agent=request.user)
    serializer = PropertyListSerializer(properties, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_transactions(request):
    """Get transactions for the current user"""

    transactions = Transaction.objects.filter(agent=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)
