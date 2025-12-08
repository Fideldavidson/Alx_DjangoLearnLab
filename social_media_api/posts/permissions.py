from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object (Post or Comment) 
    to edit or delete it. Read permissions are allowed for everyone.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only access (GET, HEAD, OPTIONS) to any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the author.
        return obj.author == request.user
