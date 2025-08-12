# api/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer

"""
Book API Views with Filtering, Searching, and Ordering

Features added:
- Filtering: filter by title, author, and publication_year.
- Searching: search in title and author's name.
- Ordering: order results by title or publication_year.
"""

class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a list of books with filtering, searching, and ordering.

    Query Parameters:
    - Filtering:
        ?title=Book+Title
        ?author=Author+Name
        ?publication_year=2023
    - Searching:
        ?search=keyword   (matches in title or author name)
    - Ordering:
        ?ordering=title
        ?ordering=-publication_year  (descending)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering options
    filterset_fields = ['title', 'author', 'publication_year']

    # Search options
    search_fields = ['title', 'author__name']

    # Ordering options
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
