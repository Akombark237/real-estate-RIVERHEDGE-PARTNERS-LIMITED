from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AboutPage, TeamMember
from .serializers import (
    AboutPageSerializer,
    AboutPageUpdateSerializer,
    TeamMemberSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    Everyone can read.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_authenticated and request.user.is_staff


class AboutPageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for About Page content.
    - GET: Anyone can view
    - PUT/PATCH: Only admins can edit
    - POST/DELETE: Not allowed (singleton pattern)
    """
    queryset = AboutPage.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return AboutPageUpdateSerializer
        return AboutPageSerializer
    
    def list(self, request, *args, **kwargs):
        """Get the About page content (singleton)"""
        instance = AboutPage.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get the About page content by ID"""
        instance = AboutPage.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update About page content (admin only)"""
        instance = AboutPage.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        
        # Track who updated
        instance.updated_by = request.user
        serializer.save()
        
        # Return full data
        return_serializer = AboutPageSerializer(instance)
        return Response(return_serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """Partially update About page content (admin only)"""
        instance = AboutPage.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Track who updated
        instance.updated_by = request.user
        serializer.save()
        
        # Return full data
        return_serializer = AboutPageSerializer(instance)
        return Response(return_serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Prevent creating new instances"""
        return Response(
            {"detail": "Cannot create new About page. Use update instead."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """Prevent deletion"""
        return Response(
            {"detail": "Cannot delete About page."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current About page content"""
        instance = AboutPage.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team Members.
    - GET: Anyone can view active members
    - POST/PUT/DELETE: Only admins
    """
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        """Return active team members for public, all for admins"""
        if self.request.user and self.request.user.is_staff:
            return TeamMember.objects.all()
        return TeamMember.objects.filter(is_active=True)

