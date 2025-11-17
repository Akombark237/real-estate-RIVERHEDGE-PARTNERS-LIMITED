from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count
from datetime import timedelta
from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentCalendarSerializer,
    AppointmentStatsSerializer
)
from activity_log.models import ActivityLog


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['appointment_type', 'status', 'priority', 'agent', 'client', 'related_property', 'is_virtual']
    search_fields = ['title', 'description', 'location', 'notes']
    ordering_fields = ['start_time', 'end_time', 'created_at', 'priority']
    ordering = ['start_time']

    def get_queryset(self):
        user = self.request.user

        # Admins see all appointments
        if user.role == 'admin':
            return Appointment.objects.all()

        # Agents see their own appointments
        if user.role == 'agent':
            return Appointment.objects.filter(
                Q(agent=user) | Q(attendees=user)
            ).distinct()

        # Clients see their own appointments
        return Appointment.objects.filter(
            Q(client=user) | Q(attendees=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AppointmentCreateSerializer
        if self.action == 'calendar':
            return AppointmentCalendarSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save(created_by=self.request.user)

        # Log activity
        ActivityLog.log_activity(
            user=self.request.user,
            action='create',
            description=f'Created appointment: {appointment.title}',
            content_object=appointment,
            severity='low'
        )

    def perform_update(self, serializer):
        appointment = serializer.save()

        # Log activity
        ActivityLog.log_activity(
            user=self.request.user,
            action='update',
            description=f'Updated appointment: {appointment.title}',
            content_object=appointment,
            severity='medium'
        )

    def perform_destroy(self, instance):
        # Log activity before deletion
        ActivityLog.log_activity(
            user=self.request.user,
            action='delete',
            description=f'Deleted appointment: {instance.title}',
            severity='high'
        )
        instance.delete()

    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Get appointments for calendar view"""
        queryset = self.filter_queryset(self.get_queryset())

        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_time__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments"""
        now = timezone.now()
        days = int(request.query_params.get('days', 7))

        queryset = self.get_queryset().filter(
            start_time__gte=now,
            start_time__lte=now + timedelta(days=days),
            status__in=['scheduled', 'confirmed']
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments"""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(
            start_time__date=today
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get appointment statistics"""
        queryset = self.get_queryset()
        now = timezone.now()

        stats = {
            'total_appointments': queryset.count(),
            'scheduled': queryset.filter(status='scheduled').count(),
            'confirmed': queryset.filter(status='confirmed').count(),
            'completed': queryset.filter(status='completed').count(),
            'cancelled': queryset.filter(status='cancelled').count(),
            'upcoming_today': queryset.filter(
                start_time__date=now.date(),
                status__in=['scheduled', 'confirmed']
            ).count(),
            'upcoming_week': queryset.filter(
                start_time__gte=now,
                start_time__lte=now + timedelta(days=7),
                status__in=['scheduled', 'confirmed']
            ).count(),
            'by_type': list(queryset.values('appointment_type').annotate(count=Count('id'))),
            'by_agent': list(queryset.values('agent__full_name').annotate(count=Count('id'))[:10])
        }

        serializer = AppointmentStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm an appointment"""
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()

        ActivityLog.log_activity(
            user=request.user,
            action='update',
            description=f'Confirmed appointment: {appointment.title}',
            content_object=appointment,
            severity='low'
        )

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()

        ActivityLog.log_activity(
            user=request.user,
            action='update',
            description=f'Cancelled appointment: {appointment.title}',
            content_object=appointment,
            severity='medium'
        )

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark appointment as completed"""
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()

        ActivityLog.log_activity(
            user=request.user,
            action='update',
            description=f'Completed appointment: {appointment.title}',
            content_object=appointment,
            severity='low'
        )

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
