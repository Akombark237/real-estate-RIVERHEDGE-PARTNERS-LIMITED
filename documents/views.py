from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, Http404
from django.db import models
from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer
from activity_log.models import ActivityLog


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document model with file upload support"""

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'document_type', 'related_property', 'related_transaction', 'related_user', 'is_archived']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['uploaded_at', 'title', 'file_size']
    ordering = ['-uploaded_at']

    def get_queryset(self):
        """Filter documents based on user permissions"""
        user = self.request.user
        queryset = Document.objects.all()

        # Non-admin users can only see their own documents or public ones
        if not user.is_staff:
            queryset = queryset.filter(
                models.Q(uploaded_by=user) |
                models.Q(is_public=True) |
                models.Q(related_property__agent=user) |
                models.Q(related_transaction__agent=user)
            ).distinct()

        return queryset

    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return DocumentUploadSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        """Create document and log activity"""
        document = serializer.save(uploaded_by=self.request.user)

        # Log activity
        ActivityLog.log_activity(
            user=self.request.user,
            action='upload',
            description=f'Uploaded document: {document.title}',
            content_object=document,
            severity='low',
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

    def perform_destroy(self, instance):
        """Delete document and log activity"""
        title = instance.title

        # Log activity before deletion
        ActivityLog.log_activity(
            user=self.request.user,
            action='delete',
            description=f'Deleted document: {title}',
            model_name='Document',
            object_repr=title,
            severity='medium',
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        instance.delete()

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download a document file"""
        document = self.get_object()

        try:
            # Log download activity
            ActivityLog.log_activity(
                user=request.user,
                action='download',
                description=f'Downloaded document: {document.title}',
                content_object=document,
                severity='low',
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            return FileResponse(document.file.open('rb'), as_attachment=True,
                              filename=document.file.name.split('/')[-1])
        except Exception as e:
            raise Http404("File not found")

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get document statistics"""
        queryset = self.get_queryset()

        stats = {
            'total_documents': queryset.count(),
            'total_size_mb': sum(doc.file_size_mb for doc in queryset),
            'by_category': {},
            'by_type': {},
            'recent_uploads': DocumentSerializer(
                queryset[:5], many=True, context={'request': request}
            ).data
        }

        # Count by category
        for category in Document.CATEGORY_CHOICES:
            count = queryset.filter(category=category[0]).count()
            if count > 0:
                stats['by_category'][category[1]] = count

        # Count by type
        for doc_type in Document.DOCUMENT_TYPE_CHOICES:
            count = queryset.filter(document_type=doc_type[0]).count()
            if count > 0:
                stats['by_type'][doc_type[1]] = count

        return Response(stats)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a document"""
        document = self.get_object()
        document.is_archived = True
        document.save()

        ActivityLog.log_activity(
            user=request.user,
            action='archive',
            description=f'Archived document: {document.title}',
            content_object=document,
            severity='low'
        )

        return Response({'status': 'archived'})

    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
