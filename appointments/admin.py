from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'appointment_type', 'agent', 'client', 'start_time', 'status', 'priority']
    list_filter = ['appointment_type', 'status', 'priority', 'is_virtual', 'start_time']
    search_fields = ['title', 'description', 'location', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'reminder_sent_at']
    date_hierarchy = 'start_time'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'appointment_type')
        }),
        ('Participants', {
            'fields': ('agent', 'client', 'attendees')
        }),
        ('Related Objects', {
            'fields': ('related_property', 'related_transaction')
        }),
        ('Scheduling', {
            'fields': ('start_time', 'end_time', 'duration_minutes')
        }),
        ('Location', {
            'fields': ('location', 'meeting_link', 'is_virtual')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Reminders', {
            'fields': ('send_reminder', 'reminder_sent', 'reminder_sent_at')
        }),
        ('Notes', {
            'fields': ('notes', 'client_notes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
