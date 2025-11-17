from django.db import models
from django.conf import settings


class Notification(models.Model):
    """In-app notification model"""
    
    TYPE_CHOICES = [
        ('transaction', 'Transaction Update'),
        ('property', 'Property Update'),
        ('price_alert', 'Price Alert'),
        ('system', 'System Notification'),
        ('assignment', 'New Assignment'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Optional reference to related objects
    related_id = models.IntegerField(null=True, blank=True, help_text="ID of related object")
    related_type = models.CharField(max_length=50, null=True, blank=True, help_text="Type of related object")
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

