from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
    """
    Model for conversations between users (client-agent messaging)
    """

    # Participants
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )

    # Subject
    subject = models.CharField(max_length=255, blank=True, null=True)

    # Related Objects
    related_property = models.ForeignKey(
        'properties.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    related_transaction = models.ForeignKey(
        'properties.Transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    related_appointment = models.ForeignKey(
        'appointments.Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )

    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Status
    is_archived = models.BooleanField(default=False)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_archived']),
        ]

    def __str__(self):
        return f"Conversation: {self.subject or f'ID {self.id}'}"

    @property
    def last_message(self):
        """Get the last message in the conversation"""
        return self.messages.order_by('-created_at').first()

    @property
    def unread_count(self, user):
        """Get unread message count for a user"""
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """
    Model for individual messages in a conversation
    """

    # Conversation
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    # Sender and Receiver
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    # Content
    message = models.TextField()

    # Attachments
    attachment = models.FileField(
        upload_to='message_attachments/',
        null=True,
        blank=True
    )
    attachment_name = models.CharField(max_length=255, blank=True, null=True)

    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"Message from {self.sender.full_name} at {self.created_at}"

    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class ClientPropertyInterest(models.Model):
    """
    Model to track which properties clients are interested in
    """

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='property_interests'
    )
    property_obj = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='client_interests'
    )

    # Interest Level
    INTEREST_LEVELS = [
        ('low', 'Low Interest'),
        ('medium', 'Medium Interest'),
        ('high', 'High Interest'),
        ('very_high', 'Very High Interest'),
    ]
    interest_level = models.CharField(max_length=20, choices=INTEREST_LEVELS, default='medium')

    # Status
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('viewing_scheduled', 'Viewing Scheduled'),
        ('offer_made', 'Offer Made'),
        ('negotiating', 'Negotiating'),
        ('purchased', 'Purchased'),
        ('not_interested', 'Not Interested'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='interested')

    # Notes
    notes = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client_property_interests'
        unique_together = ['client', 'property_obj']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client', '-created_at']),
            models.Index(fields=['property_obj']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.client.full_name} - {self.property_obj.title}"
