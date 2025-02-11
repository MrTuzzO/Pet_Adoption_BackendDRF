from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of a cat to edit or delete it.
    Assumes the Cat model has an 'author' field that relates to the User model.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        # Allow the author of the object to edit or delete it
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins (staff users) to edit or delete any object.
    - Everyone else can only read (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow admins to edit/delete any object
        return request.user.is_staff