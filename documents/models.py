from django.db import models
from django.conf import settings
import os


def get_upload_path(instance, filename):
    """Generate upload path based on document type"""
    if hasattr(instance, 'related_transaction') and instance.related_transaction:
        return f'documents/transactions/{instance.related_transaction.id}/{filename}'
    elif hasattr(instance, 'related_property') and instance.related_property:
        return f'documents/properties/{instance.related_property.id}/{filename}'
    else:
        return f'documents/general/{filename}'


class Document(models.Model):
    """Universal document model for all document types"""

    DOCUMENT_TYPE_CHOICES = [
        # Property Documents
        ('property_deed', 'Property Deed'),
        ('property_contract', 'Property Contract'),
        ('property_certificate', 'Property Certificate'),
        ('property_inspection', 'Inspection Report'),
        ('property_appraisal', 'Appraisal Report'),
        ('property_survey', 'Survey Report'),
        ('property_title', 'Title Document'),

        # Transaction Documents
        ('transaction_agreement', 'Transaction Agreement'),
        ('transaction_receipt', 'Receipt'),
        ('transaction_invoice', 'Invoice'),
        ('transaction_contract', 'Contract'),
        ('transaction_disclosure', 'Disclosure Document'),

        # General Documents
        ('identification', 'Identification'),
        ('financial', 'Financial Document'),
        ('legal', 'Legal Document'),
        ('other', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('property', 'Property'),
        ('transaction', 'Transaction'),
        ('user', 'User'),
        ('general', 'General'),
    ]

    # Basic Information
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # File
    file = models.FileField(upload_to=get_upload_path)
    file_size = models.BigIntegerField(null=True, blank=True)  # in bytes
    file_type = models.CharField(max_length=100, blank=True, null=True)  # MIME type

    # Relationships (nullable to support different document types)
    related_property = models.ForeignKey('properties.Property', on_delete=models.CASCADE,
                                 related_name='all_documents', null=True, blank=True)
    related_transaction = models.ForeignKey('properties.Transaction', on_delete=models.CASCADE,
                                    related_name='documents', null=True, blank=True)
    related_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='user_documents', null=True, blank=True)

    # Metadata
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Access Control
    is_public = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    # Tags for better organization
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'documents'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['category', '-uploaded_at']),
            models.Index(fields=['document_type']),
            models.Index(fields=['related_property', '-uploaded_at']),
            models.Index(fields=['related_transaction', '-uploaded_at']),
            models.Index(fields=['related_user', '-uploaded_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"

    def save(self, *args, **kwargs):
        # Auto-set file size and type
        if self.file:
            self.file_size = self.file.size
            # Get file extension
            ext = os.path.splitext(self.file.name)[1].lower()
            mime_types = {
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.txt': 'text/plain',
            }
            self.file_type = mime_types.get(ext, 'application/octet-stream')

        # Auto-set category based on relationships
        if not self.category:
            if self.related_property:
                self.category = 'property'
            elif self.related_transaction:
                self.category = 'transaction'
            elif self.related_user:
                self.category = 'user'
            else:
                self.category = 'general'

        super().save(*args, **kwargs)

    @property
    def file_size_mb(self):
        """Return file size in MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

    @property
    def file_extension(self):
        """Return file extension"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''
