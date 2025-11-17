"""
Custom permission classes for role-based access control
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if user is an admin
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsAgent(permissions.BasePermission):
    """
    Permission class to check if user is an agent
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'agent'


class IsClient(permissions.BasePermission):
    """
    Permission class to check if user is a client
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'client'


class IsAdminOrAgent(permissions.BasePermission):
    """
    Permission class to check if user is an admin or agent
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                request.user.role in ['admin', 'agent'])


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission class to check if user is an admin or the owner of the object
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.role == 'admin':
            return True
        
        # Check if object has a user or owner field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'agent'):
            return obj.agent == request.user
        elif hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        
        return False


class IsAgentOrOwner(permissions.BasePermission):
    """
    Permission class to check if user is an agent or the owner of the object
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Agents and admins can access
        if request.user.role in ['admin', 'agent']:
            return True
        
        # Check if user is the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'client'):
            return obj.client == request.user
        
        return False


class ReadOnly(permissions.BasePermission):
    """
    Permission class for read-only access
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow admins full access, others read-only
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class CanManageProperties(permissions.BasePermission):
    """
    Permission class for property management
    Admins and agents can create/update/delete
    Clients can only view
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Read access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write access only for admins and agents
        return request.user.role in ['admin', 'agent']

    def has_object_permission(self, request, view, obj):
        # Read access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admins can do anything
        if request.user.role == 'admin':
            return True
        
        # Agents can only modify their own properties
        if request.user.role == 'agent':
            return obj.agent == request.user
        
        return False


class CanManageTransactions(permissions.BasePermission):
    """
    Permission class for transaction management
    Admins and agents can create/update/delete
    Clients can view their own transactions
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins and agents can do anything
        if request.user.role in ['admin', 'agent']:
            return True
        
        # Clients can only view
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.role == 'admin':
            return True
        
        # Agents can manage their own transactions
        if request.user.role == 'agent':
            if request.method in permissions.SAFE_METHODS:
                return obj.agent == request.user
            return obj.agent == request.user
        
        # Clients can only view their own transactions
        if request.user.role == 'client':
            if request.method in permissions.SAFE_METHODS:
                return obj.buyer == request.user or obj.seller == request.user
        
        return False

