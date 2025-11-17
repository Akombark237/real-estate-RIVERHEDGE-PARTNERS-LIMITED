from rest_framework import serializers
from .models import AboutPage, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for Team Members"""
    
    class Meta:
        model = TeamMember
        fields = [
            'id',
            'name',
            'position',
            'bio',
            'photo',
            'email',
            'phone',
            'linkedin_url',
            'twitter_url',
            'order',
        ]
        read_only_fields = ['id']


class AboutPageSerializer(serializers.ModelSerializer):
    """Serializer for About Page content"""
    
    # Convert text fields to lists for frontend
    core_values_list = serializers.SerializerMethodField()
    services_list = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutPage
        fields = [
            'id',
            'title',
            'subtitle',
            'company_description',
            'mission',
            'vision',
            'core_values',
            'core_values_list',
            'services',
            'services_list',
            'email',
            'phone',
            'address',
            'facebook_url',
            'twitter_url',
            'linkedin_url',
            'instagram_url',
            'why_choose_us',
            'team_description',
            'years_of_experience',
            'properties_sold',
            'happy_clients',
            'team_members',
            'updated_at',
            'updated_by_name',
        ]
        read_only_fields = ['id', 'updated_at', 'updated_by_name']
    
    def get_core_values_list(self, obj):
        """Convert core values text to list"""
        if obj.core_values:
            return [value.strip() for value in obj.core_values.split('\n') if value.strip()]
        return []
    
    def get_services_list(self, obj):
        """Convert services text to list"""
        if obj.services:
            return [service.strip() for service in obj.services.split('\n') if service.strip()]
        return []
    
    def get_updated_by_name(self, obj):
        """Get name of user who last updated"""
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.email
        return None


class AboutPageUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating About Page (admin only)"""
    
    class Meta:
        model = AboutPage
        fields = [
            'title',
            'subtitle',
            'company_description',
            'mission',
            'vision',
            'core_values',
            'services',
            'email',
            'phone',
            'address',
            'facebook_url',
            'twitter_url',
            'linkedin_url',
            'instagram_url',
            'why_choose_us',
            'team_description',
            'years_of_experience',
            'properties_sold',
            'happy_clients',
            'team_members',
        ]
    
    def validate_core_values(self, value):
        """Ensure core values are properly formatted"""
        if value:
            # Clean up the text
            values = [v.strip() for v in value.split('\n') if v.strip()]
            return '\n'.join(values)
        return value
    
    def validate_services(self, value):
        """Ensure services are properly formatted"""
        if value:
            # Clean up the text
            services = [s.strip() for s in value.split('\n') if s.strip()]
            return '\n'.join(services)
        return value

