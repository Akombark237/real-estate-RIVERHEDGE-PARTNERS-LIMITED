from django.contrib import admin
from .models import AboutPage, TeamMember


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Admin interface for About Page - Only one instance allowed"""
    
    fieldsets = (
        ('Page Header', {
            'fields': ('title', 'subtitle')
        }),
        ('Company Information', {
            'fields': ('company_description', 'mission', 'vision')
        }),
        ('Core Values & Services', {
            'fields': ('core_values', 'services'),
            'description': 'Enter each value/service on a new line'
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Additional Content', {
            'fields': ('why_choose_us', 'team_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('years_of_experience', 'properties_sold', 'happy_clients', 'team_members'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('updated_at', 'updated_by')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    def save_model(self, request, obj, form, change):
        # Track who updated the page
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def changelist_view(self, request, extra_context=None):
        # If no instance exists, redirect to create one
        if not AboutPage.objects.exists():
            AboutPage.objects.create()
        return super().changelist_view(request, extra_context)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin interface for Team Members"""
    
    list_display = ('name', 'position', 'email', 'phone', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'position')
    search_fields = ('name', 'position', 'email')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'photo')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return ['created_at', 'updated_at']
        return []

