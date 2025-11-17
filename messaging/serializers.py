from rest_framework import serializers
from .models import Conversation, Message, ClientPropertyInterest
from users.serializers import UserSerializer
from properties.serializers import PropertyListSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'sender_name', 'sender_email', 'sender_role',
            'message', 'attachment', 'attachment_name',
            'is_read', 'read_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['sender', 'is_read', 'read_at', 'created_at', 'updated_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'message', 'attachment', 'attachment_name']


class ConversationSerializer(serializers.ModelSerializer):
    participants_details = UserSerializer(source='participants', many=True, read_only=True)
    last_message_text = serializers.SerializerMethodField()
    last_message_time = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    property_title = serializers.CharField(source='related_property.title', read_only=True)
    transaction_id = serializers.IntegerField(source='related_transaction.id', read_only=True)
    appointment_title = serializers.CharField(source='related_appointment.title', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'subject', 'participants', 'participants_details',
            'related_property', 'property_title',
            'related_transaction', 'transaction_id',
            'related_appointment', 'appointment_title',
            'last_message_text', 'last_message_time', 'unread_count',
            'is_archived', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_last_message_text(self, obj):
        last_msg = obj.last_message
        return last_msg.message if last_msg else None
    
    def get_last_message_time(self, obj):
        last_msg = obj.last_message
        return last_msg.created_at if last_msg else None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


class ConversationDetailSerializer(serializers.ModelSerializer):
    participants_details = UserSerializer(source='participants', many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    property_title = serializers.CharField(source='related_property.title', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'subject', 'participants', 'participants_details', 'messages',
            'related_property', 'property_title',
            'related_transaction', 'related_appointment',
            'is_archived', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            'subject', 'participants',
            'related_property', 'related_transaction', 'related_appointment'
        ]


class ClientPropertyInterestSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    property_title = serializers.CharField(source='property_obj.title', read_only=True)
    property_price = serializers.DecimalField(source='property_obj.price', max_digits=15, decimal_places=2, read_only=True)
    property_location = serializers.CharField(source='property_obj.location', read_only=True)
    property_status = serializers.CharField(source='property_obj.status', read_only=True)
    interest_level_display = serializers.CharField(source='get_interest_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ClientPropertyInterest
        fields = [
            'id', 'client', 'client_name', 'client_email',
            'property_obj', 'property_title', 'property_price', 'property_location', 'property_status',
            'interest_level', 'interest_level_display',
            'status', 'status_display',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ClientPropertyInterestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPropertyInterest
        fields = ['client', 'property_obj', 'interest_level', 'status', 'notes']


class ClientDashboardSerializer(serializers.Serializer):
    """Serializer for client dashboard data"""
    total_interests = serializers.IntegerField()
    active_transactions = serializers.IntegerField()
    upcoming_appointments = serializers.IntegerField()
    unread_messages = serializers.IntegerField()
    recent_properties = serializers.ListField()
    recent_transactions = serializers.ListField()
    upcoming_appointments_list = serializers.ListField()
    recent_messages = serializers.ListField()

