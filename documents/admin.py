from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'category', 'file_size_mb', 'uploaded_by', 'uploaded_at', 'is_archived']
    list_filter = ['category', 'document_type', 'is_archived', 'is_public', 'uploaded_at']
    search_fields = ['title', 'description', 'tags']
    readonly_fields = ['file_size', 'file_type', 'uploaded_at', 'updated_at']
    date_hierarchy = 'uploaded_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'document_type', 'category')
        }),
        ('File', {
            'fields': ('file', 'file_size', 'file_type')
        }),
        ('Relationships', {
            'fields': ('property', 'transaction', 'user')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at', 'tags')
        }),
        ('Access Control', {
            'fields': ('is_public', 'is_archived')
        }),
    )
