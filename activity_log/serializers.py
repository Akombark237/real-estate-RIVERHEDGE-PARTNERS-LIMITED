from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model"""
    
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'user_name', 'user_email', 'action', 'action_display',
            'description', 'severity', 'severity_display', 'content_type', 'object_id',
            'model_name', 'object_repr', 'changes', 'ip_address', 'user_agent',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ActivityLogCreateSerializer(serializers.Serializer):
    """Serializer for creating activity logs"""
    
    action = serializers.ChoiceField(choices=ActivityLog.ACTION_CHOICES)
    description = serializers.CharField()
    severity = serializers.ChoiceField(choices=ActivityLog.SEVERITY_CHOICES, default='low')
    model_name = serializers.CharField(required=False, allow_blank=True)
    object_repr = serializers.CharField(required=False, allow_blank=True)
    changes = serializers.JSONField(required=False)
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        ip_address = self.get_client_ip(request) if request else None
        user_agent = request.META.get('HTTP_USER_AGENT', '') if request else None
        
        return ActivityLog.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            **validated_data
        )
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

