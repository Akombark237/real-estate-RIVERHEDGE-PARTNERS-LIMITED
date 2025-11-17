from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import ActivityLog
from .serializers import ActivityLogSerializer, ActivityLogCreateSerializer


class ActivityLogViewSet(viewsets.ModelViewSet):
    """ViewSet for ActivityLog model"""

    permission_classes = [IsAuthenticated]
    serializer_class = ActivityLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'severity', 'model_name', 'user']
    search_fields = ['description', 'object_repr', 'model_name']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter activity logs based on user permissions"""
        user = self.request.user

        # Admin users can see all logs
        if user.is_staff:
            return ActivityLog.objects.all()

        # Regular users can only see their own logs
        return ActivityLog.objects.filter(user=user)

    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return ActivityLogCreateSerializer
        return ActivityLogSerializer

    def get_permissions(self):
        """Only admins can delete logs"""
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity log statistics"""
        queryset = self.get_queryset()

        # Get date range from query params (default: last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)

        recent_logs = queryset.filter(created_at__gte=start_date)

        stats = {
            'total_activities': recent_logs.count(),
            'by_action': {},
            'by_severity': {},
            'by_user': {},
            'by_model': {},
            'recent_critical': ActivityLogSerializer(
                queryset.filter(severity='critical')[:10], many=True
            ).data,
            'timeline': self.get_timeline_data(recent_logs, days)
        }

        # Count by action
        action_counts = recent_logs.values('action').annotate(count=Count('id'))
        for item in action_counts:
            action_display = dict(ActivityLog.ACTION_CHOICES).get(item['action'], item['action'])
            stats['by_action'][action_display] = item['count']

        # Count by severity
        severity_counts = recent_logs.values('severity').annotate(count=Count('id'))
        for item in severity_counts:
            severity_display = dict(ActivityLog.SEVERITY_CHOICES).get(item['severity'], item['severity'])
            stats['by_severity'][severity_display] = item['count']

        # Count by user (top 10)
        user_counts = recent_logs.exclude(user__isnull=True).values(
            'user__full_name'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        for item in user_counts:
            stats['by_user'][item['user__full_name']] = item['count']

        # Count by model (top 10)
        model_counts = recent_logs.exclude(model_name__isnull=True).values(
            'model_name'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        for item in model_counts:
            stats['by_model'][item['model_name']] = item['count']

        return Response(stats)

    @action(detail=False, methods=['get'])
    def my_activity(self, request):
        """Get current user's recent activity"""
        logs = ActivityLog.objects.filter(user=request.user)[:50]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Get critical severity logs"""
        logs = self.get_queryset().filter(severity='critical')
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def cleanup(self, request):
        """Clean up old activity logs (admin only)"""
        days = int(request.data.get('days', 90))
        cutoff_date = datetime.now() - timedelta(days=days)

        # Delete logs older than cutoff date (except critical ones)
        deleted = ActivityLog.objects.filter(
            created_at__lt=cutoff_date
        ).exclude(severity='critical').delete()

        return Response({
            'deleted': deleted[0],
            'message': f'Deleted activity logs older than {days} days'
        })

    def get_timeline_data(self, queryset, days):
        """Get activity timeline data for charts"""
        timeline = []
        for i in range(days):
            date = datetime.now().date() - timedelta(days=i)
            count = queryset.filter(created_at__date=date).count()
            timeline.append({
                'date': date.isoformat(),
                'count': count
            })
        return list(reversed(timeline))
