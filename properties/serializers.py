from rest_framework import serializers
from .models import Property, PropertyImage, PropertyDocument, Transaction


class PropertyImageSerializer(serializers.ModelSerializer):
    """Serializer for PropertyImage model"""
    
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption', 'is_primary', 'order', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class PropertyDocumentSerializer(serializers.ModelSerializer):
    """Serializer for PropertyDocument model"""
    
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    
    class Meta:
        model = PropertyDocument
        fields = ['id', 'document_type', 'title', 'file', 'description', 
                  'uploaded_by', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property model"""
    
    images = PropertyImageSerializer(many=True, read_only=True)
    documents = PropertyDocumentSerializer(many=True, read_only=True)
    agent_name = serializers.CharField(source='agent.full_name', read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'property_type', 'address', 'city', 
                  'state', 'country', 'postal_code', 'latitude', 'longitude', 
                  'price', 'currency', 'size_sqft', 'size_sqm', 'bedrooms', 
                  'bathrooms', 'year_built', 'parking_spaces', 'status', 
                  'listing_date', 'agent', 'agent_name', 'owner', 'owner_name', 
                  'features', 'images', 'documents', 'created_at', 'updated_at']
        read_only_fields = ['id', 'listing_date', 'created_at', 'updated_at']


class PropertyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for property lists"""
    
    agent_name = serializers.CharField(source='agent.full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 'title', 'property_type', 'city', 'state', 'price', 
                  'currency', 'size_sqft', 'bedrooms', 'bathrooms', 'status', 
                  'agent_name', 'primary_image', 'listing_date']
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return primary.image.url if primary.image else None
        first_image = obj.images.first()
        return first_image.image.url if first_image and first_image.image else None


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    
    property_title = serializers.CharField(source='property.title', read_only=True)
    buyer_name = serializers.CharField(source='buyer.full_name', read_only=True)
    seller_name = serializers.CharField(source='seller.full_name', read_only=True)
    agent_name = serializers.CharField(source='agent.full_name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'property', 'property_title', 'buyer', 'buyer_name', 
                  'seller', 'seller_name', 'agent', 'agent_name', 'sale_price', 
                  'commission_rate', 'commission_amount', 'status', 
                  'transaction_date', 'closing_date', 'notes', 'created_at', 
                  'updated_at']
        read_only_fields = ['id', 'commission_amount', 'created_at', 'updated_at']

