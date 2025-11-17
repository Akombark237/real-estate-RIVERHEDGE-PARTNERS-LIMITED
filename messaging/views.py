from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count, Prefetch
from datetime import timedelta
from .models import Conversation, Message, ClientPropertyInterest
from .serializers import (
    ConversationSerializer,
    ConversationDetailSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ClientPropertyInterestSerializer,
    ClientPropertyInterestCreateSerializer,
    ClientDashboardSerializer
)
from activity_log.models import ActivityLog
from properties.models import Property, Transaction
from appointments.models import Appointment


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_archived', 'related_property', 'related_transaction']
    search_fields = ['subject']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related('participants', 'messages')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        conversation = serializer.save(created_by=self.request.user)
        # Add creator to participants if not already
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

        ActivityLog.log_activity(
            user=self.request.user,
            action='create',
            description=f'Started conversation: {conversation.subject or "New conversation"}',
            content_object=conversation,
            severity='low'
        )

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a conversation"""
        conversation = self.get_object()
        conversation.is_archived = True
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        """Unarchive a conversation"""
        conversation = self.get_object()
        conversation.is_archived = False
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_all_read(self, request, pk=None):
        """Mark all messages in conversation as read"""
        conversation = self.get_object()
        messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)

        for message in messages:
            message.mark_as_read()

        return Response({'status': 'All messages marked as read'})


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation', 'sender', 'is_read']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        user = self.request.user
        # Only show messages from conversations user is part of
        return Message.objects.filter(conversation__participants=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)

        # Update conversation timestamp
        message.conversation.save()  # This triggers updated_at

        ActivityLog.log_activity(
            user=self.request.user,
            action='create',
            description=f'Sent message in conversation: {message.conversation.subject or "Conversation"}',
            content_object=message,
            severity='low'
        )

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        message.mark_as_read()

        serializer = self.get_serializer(message)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get all unread messages"""
        queryset = self.get_queryset().filter(is_read=False).exclude(sender=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClientPropertyInterestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['client', 'property_obj', 'interest_level', 'status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Admins and agents see all
        if user.role in ['admin', 'agent']:
            return ClientPropertyInterest.objects.all()

        # Clients see only their own
        return ClientPropertyInterest.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClientPropertyInterestCreateSerializer
        return ClientPropertyInterestSerializer

    def perform_create(self, serializer):
        interest = serializer.save()

        ActivityLog.log_activity(
            user=self.request.user,
            action='create',
            description=f'Expressed interest in property: {interest.property_obj.title}',
            content_object=interest,
            severity='low'
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_dashboard(request):
    """
    Get client dashboard data with all relevant information
    """
    user = request.user

    # Only clients can access this
    if user.role != 'client':
        return Response({'error': 'This endpoint is only for clients'}, status=403)

    now = timezone.now()

    # Get statistics
    total_interests = ClientPropertyInterest.objects.filter(client=user).count()
    active_transactions = Transaction.objects.filter(
        Q(buyer=user) | Q(seller=user),
        status__in=['pending', 'in_progress']
    ).count()
    upcoming_appointments = Appointment.objects.filter(
        Q(client=user) | Q(attendees=user),
        start_time__gte=now,
        status__in=['scheduled', 'confirmed']
    ).count()
    unread_messages = Message.objects.filter(
        conversation__participants=user,
        is_read=False
    ).exclude(sender=user).count()

    # Get recent properties (interested in)
    recent_interests = ClientPropertyInterest.objects.filter(
        client=user
    ).select_related('property_obj').order_by('-created_at')[:5]

    recent_properties = []
    for interest in recent_interests:
        recent_properties.append({
            'id': interest.property_obj.id,
            'title': interest.property_obj.title,
            'price': str(interest.property_obj.price),
            'location': interest.property_obj.location,
            'status': interest.property_obj.status,
            'interest_level': interest.interest_level,
            'interest_status': interest.status,
        })

    # Get recent transactions
    recent_transactions_qs = Transaction.objects.filter(
        Q(buyer=user) | Q(seller=user)
    ).select_related('property_obj').order_by('-created_at')[:5]

    recent_transactions = []
    for trans in recent_transactions_qs:
        recent_transactions.append({
            'id': trans.id,
            'property_title': trans.property_obj.title,
            'amount': str(trans.amount),
            'status': trans.status,
            'transaction_type': trans.transaction_type,
            'created_at': trans.created_at,
        })

    # Get upcoming appointments
    upcoming_appointments_qs = Appointment.objects.filter(
        Q(client=user) | Q(attendees=user),
        start_time__gte=now,
        status__in=['scheduled', 'confirmed']
    ).select_related('agent', 'related_property').order_by('start_time')[:5]

    upcoming_appointments_list = []
    for appt in upcoming_appointments_qs:
        upcoming_appointments_list.append({
            'id': appt.id,
            'title': appt.title,
            'appointment_type': appt.appointment_type,
            'start_time': appt.start_time,
            'agent_name': appt.agent.full_name,
            'property_title': appt.related_property.title if appt.related_property else None,
            'location': appt.location,
            'is_virtual': appt.is_virtual,
        })

    # Get recent messages
    recent_messages_qs = Message.objects.filter(
        conversation__participants=user
    ).select_related('sender', 'conversation').order_by('-created_at')[:10]

    recent_messages = []
    for msg in recent_messages_qs:
        recent_messages.append({
            'id': msg.id,
            'conversation_id': msg.conversation.id,
            'conversation_subject': msg.conversation.subject,
            'sender_name': msg.sender.full_name,
            'message': msg.message[:100],  # First 100 chars
            'is_read': msg.is_read,
            'created_at': msg.created_at,
        })

    # Prepare dashboard data
    dashboard_data = {
        'total_interests': total_interests,
        'active_transactions': active_transactions,
        'upcoming_appointments': upcoming_appointments,
        'unread_messages': unread_messages,
        'recent_properties': recent_properties,
        'recent_transactions': recent_transactions,
        'upcoming_appointments_list': upcoming_appointments_list,
        'recent_messages': recent_messages,
    }

    serializer = ClientDashboardSerializer(dashboard_data)
    return Response(serializer.data)
