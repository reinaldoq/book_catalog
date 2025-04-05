from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission

from users.enums import UserRole
from .models import Book
from .serializers import BookSerializer


class IsEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for any authenticated user
        if request.method in SAFE_METHODS:
            return True
        # Only users with the 'editor' role can write
        return request.user.role == UserRole.EDITOR


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated, IsEditorOrReadOnly]
