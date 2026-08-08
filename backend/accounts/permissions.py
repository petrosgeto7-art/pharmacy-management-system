from rest_framework import permissions

class HasPermission(permissions.BasePermission):
    """
    Custom permission class to check if a user has a specific permission based on their role.
    Usage in views:
    permission_classes = [HasPermission('medicines.view')]
    """
    
    def __init__(self, required_permission=None):
        self.required_permission = required_permission
        
    def __call__(self):
        return self

    def has_permission(self, request, view):
        # Always allow superusers or admins
        if request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin):
            return True
            
        if not request.user or not request.user.is_authenticated:
            return False
            
        # If no specific permission is required, just need authentication
        if not self.required_permission:
            return True
            
        # For viewsets, we can determine required permission based on action
        if hasattr(view, 'action') and view.action:
            # Map common actions to permissions
            action_map = {
                'list': 'view',
                'retrieve': 'view',
                'create': 'create',
                'update': 'edit',
                'partial_update': 'edit',
                'destroy': 'delete',
            }
            
            # Use view's specific permission prefix if defined
            perm_prefix = getattr(view, 'permission_prefix', None)
            
            if perm_prefix and view.action in action_map:
                dynamic_perm = f"{perm_prefix}.{action_map[view.action]}"
                return request.user.has_perm_custom(dynamic_perm)
                
        # Fallback to the statically provided permission
        return request.user.has_perm_custom(self.required_permission)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admin to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_superuser or request.user.is_admin)

def require_permission(perm_string):
    """Factory function to return an instantiated permission class"""
    class _RequirePermission(HasPermission):
        def __init__(self):
            super().__init__(perm_string)
    return _RequirePermission
