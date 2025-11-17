from rest_framework import serializers
from .models import Supplier, Material, MaterialPrice, PriceAlert


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model"""
    
    class Meta:
        model = Supplier
        fields = '__all__'


class MaterialPriceSerializer(serializers.ModelSerializer):
    """Serializer for MaterialPrice model"""
    
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    
    class Meta:
        model = MaterialPrice
        fields = ['id', 'material', 'material_name', 'supplier', 'supplier_name', 
                  'price', 'currency', 'region', 'source', 'recorded_at', 'notes']
        read_only_fields = ['id', 'recorded_at']


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for Material model"""
    
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    recent_prices = MaterialPriceSerializer(many=True, read_only=True, source='prices')
    
    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'unit', 'description', 'image', 
                  'is_active', 'current_price', 'average_price', 'recent_prices',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Limit recent_prices to last 5 entries
        if 'recent_prices' in representation:
            representation['recent_prices'] = representation['recent_prices'][:5]
        return representation


class MaterialListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for material lists"""
    
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'unit', 'current_price', 'is_active']


class PriceAlertSerializer(serializers.ModelSerializer):
    """Serializer for PriceAlert model"""
    
    material_name = serializers.CharField(source='material.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = PriceAlert
        fields = ['id', 'user', 'user_email', 'material', 'material_name', 
                  'alert_type', 'threshold_value', 'is_active', 'last_triggered', 
                  'created_at']
        read_only_fields = ['id', 'last_triggered', 'created_at']

