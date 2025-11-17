from django.contrib import admin
from .models import Conversation, Message, ClientPropertyInterest


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['sender', 'created_at', 'read_at']
    fields = ['sender', 'message', 'is_read', 'created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_by', 'is_archived', 'created_at', 'updated_at']
    list_filter = ['is_archived', 'created_at']
    search_fields = ['subject']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['participants']
    inlines = [MessageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('subject', 'participants')
        }),
        ('Related Objects', {
            'fields': ('related_property', 'related_transaction', 'related_appointment')
        }),
        ('Status', {
            'fields': ('is_archived',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message', 'sender__email']
    readonly_fields = ['sender', 'created_at', 'updated_at', 'read_at']

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(ClientPropertyInterest)
class ClientPropertyInterestAdmin(admin.ModelAdmin):
    list_display = ['client', 'property_obj', 'interest_level', 'status', 'created_at']
    list_filter = ['interest_level', 'status', 'created_at']
    search_fields = ['client__email', 'property_obj__title', 'notes']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('client', 'property_obj')
        }),
        ('Interest Details', {
            'fields': ('interest_level', 'status', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
