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
