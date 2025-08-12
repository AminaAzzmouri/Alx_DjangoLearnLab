from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

"""
This file defines API views for the Book model using Django REST Framework's
generic views.

Generic views simplify CRUD (Create, Read, Update, Delete) operations by combining
common patterns into reusable classes.

Views implemented:
- BookListView: List all books (GET)
- BookDetailView: Retrieve a single book by ID (GET)
- BookCreateView: Add a new book (POST)
- BookUpdateView: Update an existing book (PUT/PATCH)
- BookDeleteView: Delete a book (DELETE)
"""


class BookListView(generics.ListAPIView):
    """
    GET /books/
    Returns a list of all books in the database.

    Custom behavior:
    - Allows optional filtering by:
      ?year=YYYY → returns books published in that year
      ?author_id=N → returns books by a specific author
    Example:
      /api/books/?year=2020
      /api/books/?author_id=1

    Permissions:
    - Anyone can view the book list.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Optionally filters books by 'year' and/or 'author_id'
        based on query parameters.
        """
        queryset = Book.objects.all()
        year = self.request.query_params.get('year')
        author_id = self.request.query_params.get('author_id')

        if year:
            queryset = queryset.filter(publication_year=year)
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<id>/
    Returns details of a single book based on its ID.

    Permissions:
    - AllowAny: Anyone can view book details.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    
    """
    POST /books/create/
    Creates a new book record.

    Permissions:
    - IsAuthenticated: Only logged-in users can create books.

    Custom behavior:
    - Data validation is handled automatically by BookSerializer.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<id>/update/
    Updates details of an existing book.

    Permissions:
    - IsAuthenticated: Only logged-in users can update books.

    Custom behavior:
    - Partial updates allowed with PATCH method.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<id>/delete/
    Deletes a book from the database.

    Permissions:
    - IsAuthenticated: Only logged-in users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
