from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_repr', 'severity', 'created_at']
    list_filter = ['action', 'severity', 'model_name', 'created_at']
    search_fields = ['description', 'object_repr', 'user__email', 'user__full_name']
    readonly_fields = ['user', 'action', 'description', 'severity', 'content_type',
                      'object_id', 'model_name', 'object_repr', 'changes',
                      'ip_address', 'user_agent', 'created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        """Prevent manual creation of logs"""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent editing of logs"""
        return False
