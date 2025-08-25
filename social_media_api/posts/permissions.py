from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Allow read for all authenticated users; write only for the owner.
    (Project default permission is IsAuthenticated, so guests are blocked.)
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Post has .author, Comment has .author
        return getattr(obj, 'author_id', None) == request.user.id
