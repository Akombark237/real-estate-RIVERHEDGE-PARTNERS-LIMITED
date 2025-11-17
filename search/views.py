from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from properties.models import Property, Transaction
from materials.models import Material
from users.models import User
from documents.models import Document
from properties.serializers import PropertyListSerializer, TransactionSerializer
from materials.serializers import MaterialSerializer
from users.serializers import UserSerializer
from documents.serializers import DocumentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def global_search(request):
    """
    Global search across all models
    Query params:
        - q: search query
        - models: comma-separated list of models to search (properties,transactions,materials,users,documents)
        - limit: max results per model (default: 10)
    """
    query = request.query_params.get('q', '').strip()
    models_to_search = request.query_params.get('models', 'properties,transactions,materials,users,documents').split(',')
    limit = int(request.query_params.get('limit', 10))

    if not query:
        return Response({
            'query': '',
            'results': {},
            'total': 0
        })

    results = {}
    total = 0

    # Search Properties
    if 'properties' in models_to_search:
        properties = Property.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        )[:limit]
        results['properties'] = {
            'count': properties.count(),
            'data': PropertyListSerializer(properties, many=True, context={'request': request}).data
        }
        total += properties.count()

    # Search Transactions
    if 'transactions' in models_to_search:
        transactions = Transaction.objects.filter(
            Q(property__title__icontains=query) |
            Q(notes__icontains=query) |
            Q(buyer__full_name__icontains=query) |
            Q(seller__full_name__icontains=query)
        )[:limit]
        results['transactions'] = {
            'count': transactions.count(),
            'data': TransactionSerializer(transactions, many=True).data
        }
        total += transactions.count()

    # Search Materials
    if 'materials' in models_to_search:
        materials = Material.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(supplier__icontains=query)
        )[:limit]
        results['materials'] = {
            'count': materials.count(),
            'data': MaterialSerializer(materials, many=True).data
        }
        total += materials.count()

    # Search Users (admin only)
    if 'users' in models_to_search and request.user.is_staff:
        users = User.objects.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )[:limit]
        results['users'] = {
            'count': users.count(),
            'data': UserSerializer(users, many=True).data
        }
        total += users.count()

    # Search Documents
    if 'documents' in models_to_search:
        documents = Document.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

        # Filter by user permissions
        if not request.user.is_staff:
            documents = documents.filter(
                Q(uploaded_by=request.user) |
                Q(is_public=True) |
                Q(related_property__agent=request.user) |
                Q(related_transaction__agent=request.user)
            ).distinct()

        documents = documents[:limit]
        results['documents'] = {
            'count': documents.count(),
            'data': DocumentSerializer(documents, many=True, context={'request': request}).data
        }
        total += documents.count()

    return Response({
        'query': query,
        'results': results,
        'total': total
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_suggestions(request):
    """
    Get search suggestions based on partial query
    """
    query = request.query_params.get('q', '').strip()
    limit = int(request.query_params.get('limit', 5))

    if not query or len(query) < 2:
        return Response({'suggestions': []})

    suggestions = []

    # Property titles
    properties = Property.objects.filter(title__icontains=query).values_list('title', flat=True)[:limit]
    suggestions.extend([{'text': title, 'type': 'property'} for title in properties])

    # Cities
    cities = Property.objects.filter(city__icontains=query).values_list('city', flat=True).distinct()[:limit]
    suggestions.extend([{'text': city, 'type': 'location'} for city in cities])

    # Material names
    materials = Material.objects.filter(name__icontains=query).values_list('name', flat=True)[:limit]
    suggestions.extend([{'text': name, 'type': 'material'} for name in materials])

    return Response({'suggestions': suggestions[:limit]})
