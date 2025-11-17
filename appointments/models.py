from django.db import models
from django.conf import settings
from django.utils import timezone


class Appointment(models.Model):
    """
    Model for scheduling appointments (property viewings, meetings, etc.)
    """

    APPOINTMENT_TYPES = [
        ('property_viewing', 'Property Viewing'),
        ('meeting', 'Meeting'),
        ('consultation', 'Consultation'),
        ('inspection', 'Property Inspection'),
        ('signing', 'Document Signing'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
        ('no_show', 'No Show'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Basic Information
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    appointment_type = models.CharField(max_length=50, choices=APPOINTMENT_TYPES, default='meeting')

    # Participants
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agent_appointments',
        help_text='Agent handling the appointment'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_appointments',
        null=True,
        blank=True,
        help_text='Client attending the appointment'
    )
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='appointments_attending',
        blank=True,
        help_text='Additional attendees'
    )

    # Related Objects
    related_property = models.ForeignKey(
        'properties.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    related_transaction = models.ForeignKey(
        'properties.Transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )

    # Scheduling
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60, help_text='Duration in minutes')

    # Location
    location = models.CharField(max_length=500, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True, help_text='Online meeting link (Zoom, Teams, etc.)')
    is_virtual = models.BooleanField(default=False)

    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Reminders
    send_reminder = models.BooleanField(default=True)
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    # Notes
    notes = models.TextField(blank=True, null=True, help_text='Internal notes')
    client_notes = models.TextField(blank=True, null=True, help_text='Notes visible to client')

    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_appointments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
            models.Index(fields=['agent', 'start_time']),
            models.Index(fields=['client', 'start_time']),
            models.Index(fields=['status']),
            models.Index(fields=['appointment_type']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_past(self):
        """Check if appointment is in the past"""
        return self.end_time < timezone.now()

    @property
    def is_upcoming(self):
        """Check if appointment is upcoming (within next 24 hours)"""
        now = timezone.now()
        return self.start_time > now and self.start_time <= now + timezone.timedelta(hours=24)

    @property
    def is_today(self):
        """Check if appointment is today"""
        return self.start_time.date() == timezone.now().date()

    @property
    def duration_display(self):
        """Get human-readable duration"""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
        return f"{minutes}m"

    def save(self, *args, **kwargs):
        # Calculate duration if not set
        if not self.duration_minutes and self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_minutes = int(delta.total_seconds() / 60)

        # Set end_time if not set
        if not self.end_time and self.start_time and self.duration_minutes:
            self.end_time = self.start_time + timezone.timedelta(minutes=self.duration_minutes)

        super().save(*args, **kwargs)
