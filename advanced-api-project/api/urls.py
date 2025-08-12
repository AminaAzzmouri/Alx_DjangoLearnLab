from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

"""
API URL configuration for the Book model.

Endpoints:
- GET    /books/               → List all books (optional filters: year, author_id)
- GET    /books/<id>/          → Retrieve book details
- POST   /books/create/        → Create new book (authenticated only)
- PUT    /books/<id>/update/   → Full update of a book (authenticated only)
- PATCH  /books/<id>/update/   → Partial update of a book (authenticated only)
- DELETE /books/<id>/delete/   → Delete a book (authenticated only)
"""

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
