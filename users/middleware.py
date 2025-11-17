"""
Custom middleware for role-based access control and activity logging
"""
from django.utils.deprecation import MiddlewareMixin
from activity_log.models import ActivityLog


class RoleBasedAccessMiddleware(MiddlewareMixin):
    """
    Middleware to enforce role-based access control
    """
    
    # Define protected paths and required roles
    PROTECTED_PATHS = {
        '/admin/': ['admin'],
        '/api/users/': ['admin'],
        '/api/activity-logs/cleanup/': ['admin'],
    }
    
    def process_request(self, request):
        """
        Check if user has required role for the requested path
        """
        if not request.user.is_authenticated:
            return None
        
        path = request.path
        
        # Check if path requires specific roles
        for protected_path, required_roles in self.PROTECTED_PATHS.items():
            if path.startswith(protected_path):
                if request.user.role not in required_roles:
                    from django.http import JsonResponse
                    return JsonResponse(
                        {'error': f'Access denied. Required roles: {", ".join(required_roles)}'},
                        status=403
                    )
        
        return None


class ActivityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log user activities
    """
    
    # Paths to log
    LOG_PATHS = [
        '/api/properties/',
        '/api/transactions/',
        '/api/documents/',
        '/api/materials/',
        '/api/estimates/',
    ]
    
    # Methods to log
    LOG_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    
    def process_response(self, request, response):
        """
        Log user activities after successful requests
        """
        if not request.user.is_authenticated:
            return response
        
        # Only log successful requests
        if response.status_code not in [200, 201, 204]:
            return response
        
        path = request.path
        method = request.method
        
        # Check if we should log this request
        should_log = False
        for log_path in self.LOG_PATHS:
            if path.startswith(log_path):
                should_log = True
                break
        
        if not should_log or method not in self.LOG_METHODS:
            return response
        
        # Determine action based on method
        action_map = {
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }
        action = action_map.get(method, 'other')
        
        # Determine severity based on action
        severity_map = {
            'create': 'low',
            'update': 'medium',
            'delete': 'high',
        }
        severity = severity_map.get(action, 'low')
        
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create description
        description = f'{method} request to {path}'
        
        # Log the activity
        try:
            ActivityLog.log_activity(
                user=request.user,
                action=action,
                description=description,
                severity=severity,
                ip_address=ip_address,
                user_agent=user_agent
            )
        except Exception as e:
            # Don't fail the request if logging fails
            print(f"Failed to log activity: {str(e)}")
        
        return response


class UserLastActivityMiddleware(MiddlewareMixin):
    """
    Middleware to track user's last activity time
    """
    
    def process_request(self, request):
        """
        Update user's last activity timestamp
        """
        if request.user.is_authenticated:
            from django.utils import timezone
            # Update last_login field as a proxy for last activity
            # You could add a custom last_activity field to the User model
            request.user.last_login = timezone.now()
            request.user.save(update_fields=['last_login'])
        
        return None


class RoleContextMiddleware(MiddlewareMixin):
    """
    Middleware to add role context to requests
    """
    
    def process_request(self, request):
        """
        Add role-based context to the request
        """
        if request.user.is_authenticated:
            # Add role flags for easy checking in views
            request.is_admin = request.user.role == 'admin'
            request.is_agent = request.user.role == 'agent'
            request.is_client = request.user.role == 'client'
            request.is_staff_member = request.user.role in ['admin', 'agent']
        else:
            request.is_admin = False
            request.is_agent = False
            request.is_client = False
            request.is_staff_member = False
        
        return None

