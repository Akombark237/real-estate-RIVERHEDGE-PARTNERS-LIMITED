from rest_framework import serializers
from .models import CostEstimate, EstimateItem, ProjectTemplate


class EstimateItemSerializer(serializers.ModelSerializer):
    """Serializer for EstimateItem model"""
    
    material_name = serializers.CharField(source='material.name', read_only=True)
    
    class Meta:
        model = EstimateItem
        fields = ['id', 'estimate', 'material', 'material_name', 'item_name', 
                  'description', 'category', 'quantity', 'unit', 'unit_price', 
                  'total_price', 'labor_hours', 'labor_rate', 'notes', 'order', 
                  'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']


class CostEstimateSerializer(serializers.ModelSerializer):
    """Serializer for CostEstimate model"""
    
    items = EstimateItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)
    
    class Meta:
        model = CostEstimate
        fields = ['id', 'project_name', 'project_type', 'quality_level', 'property', 
                  'property_title', 'user', 'user_name', 'total_area_sqft', 
                  'total_area_sqm', 'material_cost', 'labor_cost', 'equipment_cost', 
                  'overhead_cost', 'total_cost', 'currency', 'status', 'estimate_date', 
                  'valid_until', 'description', 'notes', 'items', 'created_at', 
                  'updated_at']
        read_only_fields = ['id', 'material_cost', 'total_cost', 'estimate_date', 
                           'created_at', 'updated_at']


class CostEstimateListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for estimate lists"""
    
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CostEstimate
        fields = ['id', 'project_name', 'project_type', 'quality_level', 'user_name', 
                  'total_cost', 'currency', 'status', 'estimate_date', 'items_count']
    
    def get_items_count(self, obj):
        return obj.items.count()


class ProjectTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ProjectTemplate model"""
    
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = ProjectTemplate
        fields = ['id', 'name', 'description', 'project_type', 'quality_level', 
                  'default_area_sqft', 'estimated_duration_days', 'template_items', 
                  'is_active', 'created_by', 'created_by_name', 'created_at', 
                  'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

