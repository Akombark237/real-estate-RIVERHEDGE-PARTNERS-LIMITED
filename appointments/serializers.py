from rest_framework import serializers
from .models import Appointment
from users.serializers import UserSerializer
from properties.serializers import PropertyListSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.full_name', read_only=True)
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    property_title = serializers.CharField(source='related_property.title', read_only=True)
    transaction_property = serializers.CharField(source='related_transaction.property.title', read_only=True)
    duration_display = serializers.CharField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    is_today = serializers.BooleanField(read_only=True)
    appointment_type_display = serializers.CharField(source='get_appointment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'title', 'description', 'appointment_type', 'appointment_type_display',
            'agent', 'agent_name', 'client', 'client_name',
            'related_property', 'property_title', 'related_transaction', 'transaction_property',
            'start_time', 'end_time', 'duration_minutes', 'duration_display',
            'location', 'meeting_link', 'is_virtual',
            'status', 'status_display', 'priority', 'priority_display',
            'send_reminder', 'reminder_sent', 'reminder_sent_at',
            'notes', 'client_notes',
            'is_past', 'is_upcoming', 'is_today',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'reminder_sent', 'reminder_sent_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'title', 'description', 'appointment_type',
            'agent', 'client', 'related_property', 'related_transaction',
            'start_time', 'end_time', 'duration_minutes',
            'location', 'meeting_link', 'is_virtual',
            'status', 'priority', 'send_reminder',
            'notes', 'client_notes'
        ]
    
    def validate(self, data):
        """Validate appointment data"""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        # Validate time range
        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time")
        
        # Check for conflicts (optional - can be enabled)
        # agent = data.get('agent')
        # if agent and start_time and end_time:
        #     conflicts = Appointment.objects.filter(
        #         agent=agent,
        #         status__in=['scheduled', 'confirmed'],
        #         start_time__lt=end_time,
        #         end_time__gt=start_time
        #     )
        #     if self.instance:
        #         conflicts = conflicts.exclude(pk=self.instance.pk)
        #     if conflicts.exists():
        #         raise serializers.ValidationError("Agent has a conflicting appointment")
        
        return data


class AppointmentCalendarSerializer(serializers.ModelSerializer):
    """Simplified serializer for calendar view"""
    agent_name = serializers.CharField(source='agent.full_name', read_only=True)
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    property_title = serializers.CharField(source='related_property.title', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'title', 'appointment_type', 'status', 'priority',
            'agent', 'agent_name', 'client', 'client_name',
            'property_title', 'start_time', 'end_time',
            'location', 'is_virtual'
        ]


class AppointmentStatsSerializer(serializers.Serializer):
    """Serializer for appointment statistics"""
    total_appointments = serializers.IntegerField()
    scheduled = serializers.IntegerField()
    confirmed = serializers.IntegerField()
    completed = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    upcoming_today = serializers.IntegerField()
    upcoming_week = serializers.IntegerField()
    by_type = serializers.ListField()
    by_agent = serializers.ListField()

