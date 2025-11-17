from django.db import models
from django.core.validators import URLValidator


class AboutPage(models.Model):
    """
    Model for About Page content - editable by admin only
    Only one instance should exist (singleton pattern)
    """
    # Main content sections
    title = models.CharField(max_length=200, default="About RIVERHEDGE PARTNERS LIMITED")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Short tagline or subtitle")
    
    # Company overview
    company_description = models.TextField(
        help_text="Main description of the company",
        default="RIVERHEDGE PARTNERS LIMITED is a leading real estate company..."
    )
    
    # Mission and Vision
    mission = models.TextField(blank=True, help_text="Company mission statement")
    vision = models.TextField(blank=True, help_text="Company vision statement")
    
    # Core values (stored as text, one per line)
    core_values = models.TextField(
        blank=True,
        help_text="Enter core values, one per line"
    )
    
    # Services offered
    services = models.TextField(
        blank=True,
        help_text="Enter services offered, one per line"
    )
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    
    # Social media links
    facebook_url = models.URLField(blank=True, validators=[URLValidator()])
    twitter_url = models.URLField(blank=True, validators=[URLValidator()])
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()])
    instagram_url = models.URLField(blank=True, validators=[URLValidator()])
    
    # Additional sections
    why_choose_us = models.TextField(
        blank=True,
        help_text="Why customers should choose your company"
    )
    
    team_description = models.TextField(
        blank=True,
        help_text="Description of your team"
    )
    
    # Statistics
    years_of_experience = models.IntegerField(default=0, help_text="Years in business")
    properties_sold = models.IntegerField(default=0, help_text="Total properties sold")
    happy_clients = models.IntegerField(default=0, help_text="Number of satisfied clients")
    team_members = models.IntegerField(default=0, help_text="Number of team members")
    
    # Meta
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='about_page_updates'
    )
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"
    
    def __str__(self):
        return f"About Page (Last updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton)
        if not self.pk and AboutPage.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            existing = AboutPage.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        instance, created = cls.objects.get_or_create(pk=1)
        return instance


class TeamMember(models.Model):
    """Model for team members displayed on About page"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    
    # Social media
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Display order
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return f"{self.name} - {self.position}"

