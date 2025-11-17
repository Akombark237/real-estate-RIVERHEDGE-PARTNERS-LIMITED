"""
Custom decorators for role-based access control
"""
from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def admin_required(view_func):
    """
    Decorator to require admin role
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.role != 'admin':
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return view_func(request, *args, **kwargs)
    return wrapper


def agent_required(view_func):
    """
    Decorator to require agent role
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.role != 'agent':
            return Response(
                {'error': 'Agent access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_or_agent_required(view_func):
    """
    Decorator to require admin or agent role
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.role not in ['admin', 'agent']:
            return Response(
                {'error': 'Admin or Agent access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    """
    Decorator to require specific roles
    Usage: @role_required('admin', 'agent')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if request.user.role not in roles:
                return Response(
                    {'error': f'Access denied. Required roles: {", ".join(roles)}'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def check_permission(permission_func):
    """
    Decorator to check custom permission function
    Usage: @check_permission(lambda user, obj: user.id == obj.owner_id)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get object if pk is in kwargs
            obj = None
            if 'pk' in kwargs:
                # This is a simplified version - in real use, you'd get the object from the view
                pass
            
            if not permission_func(request.user, obj):
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Helper functions for permission checks
def can_manage_property(user, property_obj):
    """Check if user can manage a property"""
    if user.role == 'admin':
        return True
    if user.role == 'agent' and property_obj.agent == user:
        return True
    return False


def can_view_property(user, property_obj):
    """Check if user can view a property"""
    # All authenticated users can view properties
    return user.is_authenticated


def can_manage_transaction(user, transaction_obj):
    """Check if user can manage a transaction"""
    if user.role == 'admin':
        return True
    if user.role == 'agent' and transaction_obj.agent == user:
        return True
    return False


def can_view_transaction(user, transaction_obj):
    """Check if user can view a transaction"""
    if user.role == 'admin':
        return True
    if user.role == 'agent' and transaction_obj.agent == user:
        return True
    if user.role == 'client' and (transaction_obj.buyer == user or transaction_obj.seller == user):
        return True
    return False


def can_manage_document(user, document_obj):
    """Check if user can manage a document"""
    if user.role == 'admin':
        return True
    if document_obj.uploaded_by == user:
        return True
    return False


def can_view_document(user, document_obj):
    """Check if user can view a document"""
    if user.role == 'admin':
        return True
    if document_obj.uploaded_by == user:
        return True
    if document_obj.is_public:
        return True
    if hasattr(document_obj, 'related_property') and document_obj.related_property:
        if document_obj.related_property.agent == user:
            return True
    if hasattr(document_obj, 'related_transaction') and document_obj.related_transaction:
        if document_obj.related_transaction.agent == user:
            return True
        if document_obj.related_transaction.buyer == user or document_obj.related_transaction.seller == user:
            return True
    return False

