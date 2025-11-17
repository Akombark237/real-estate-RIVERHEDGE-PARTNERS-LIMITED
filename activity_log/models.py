from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ActivityLog(models.Model):
    """Activity log for tracking all user actions"""

    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('view', 'Viewed'),
        ('login', 'Logged In'),
        ('logout', 'Logged Out'),
        ('upload', 'Uploaded'),
        ('download', 'Downloaded'),
        ('export', 'Exported'),
        ('import', 'Imported'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('assign', 'Assigned'),
        ('unassign', 'Unassigned'),
        ('archive', 'Archived'),
        ('restore', 'Restored'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # User who performed the action
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                            null=True, related_name='activity_logs')

    # Action details
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')

    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Additional context
    model_name = models.CharField(max_length=100, blank=True, null=True)
    object_repr = models.CharField(max_length=500, blank=True, null=True)  # String representation of object

    # Changes tracking (for update actions)
    changes = models.JSONField(default=dict, blank=True)  # Store old and new values

    # Request metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['model_name', '-created_at']),
            models.Index(fields=['severity', '-created_at']),
        ]

    def __str__(self):
        user_name = self.user.full_name if self.user else 'Unknown'
        return f"{user_name} {self.get_action_display()} {self.model_name or 'item'} at {self.created_at}"

    @classmethod
    def log_activity(cls, user, action, description, content_object=None, changes=None,
                     severity='low', ip_address=None, user_agent=None):
        """Helper method to create activity log entries"""
        log_data = {
            'user': user,
            'action': action,
            'description': description,
            'severity': severity,
            'ip_address': ip_address,
            'user_agent': user_agent,
        }

        if content_object:
            log_data['content_object'] = content_object
            log_data['model_name'] = content_object.__class__.__name__
            log_data['object_repr'] = str(content_object)

        if changes:
            log_data['changes'] = changes

        return cls.objects.create(**log_data)
