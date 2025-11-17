from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    file_size_mb = serializers.FloatField(read_only=True)
    file_extension = serializers.CharField(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    # Related object names
    property_title = serializers.CharField(source='related_property.title', read_only=True)
    transaction_property = serializers.CharField(source='related_transaction.property.title', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'document_type', 'category',
            'file', 'file_url', 'file_size', 'file_size_mb', 'file_type', 'file_extension',
            'related_property', 'property_title', 'related_transaction', 'transaction_property',
            'related_user', 'uploaded_by', 'uploaded_by_name', 'uploaded_at', 'updated_at',
            'is_public', 'is_archived', 'tags'
        ]
        read_only_fields = ['id', 'file_size', 'file_type', 'uploaded_at', 'updated_at']
    
    def get_file_url(self, obj):
        """Get the full URL for the file"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class DocumentUploadSerializer(serializers.ModelSerializer):
    """Simplified serializer for document upload"""
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'document_type', 'category', 'file',
                  'related_property', 'related_transaction', 'related_user', 'tags', 'is_public']
        
    def create(self, validated_data):
        # Set uploaded_by from request user
        request = self.context.get('request')
        if request and request.user:
            validated_data['uploaded_by'] = request.user
        return super().create(validated_data)

