from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

"""
Unit Tests for the Book API endpoints.

Covers:
- CRUD operations (Create, Retrieve, Update, Delete)
- Filtering, Searching, and Ordering
- Permissions and Authentication checks
"""

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books
        self.book1 = Book.objects.create(title="Alpha Book", author=self.author1, publication_year=2020)
        self.book2 = Book.objects.create(title="Beta Book", author=self.author2, publication_year=2021)

        # URLs
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

    def test_list_books(self):
        """Test listing books without authentication (read-only allowed)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        """Test creating a book when authenticated"""
        self.client.login(username="testuser", password="password123")
        data = {
            "title": "New Book",
            "author": self.author1.id,
            "publication_year": 2022
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should be denied)"""
        data = {
            "title": "Unauthorized Book",
            "author": self.author1.id,
            "publication_year": 2022
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Test updating a book when authenticated"""
        self.client.login(username="testuser", password="password123")
        data = {
            "title": "Updated Alpha Book",
            "author": self.author1.id,
            "publication_year": 2025
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Alpha Book")

    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication (should be denied)"""
        data = {
            "title": "Fail Update",
            "author": self.author1.id,
            "publication_year": 2025
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """Test deleting a book when authenticated"""
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication (should be denied)"""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_title(self):
        """Test filtering books by exact title"""
        response = self.client.get(f"{self.list_url}?title=Alpha Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Alpha Book")

    def test_search_books(self):
        """Test searching books by keyword"""
        response = self.client.get(f"{self.list_url}?search=Beta")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Beta Book")

    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year descending"""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Beta Book")  # 2021 comes before 2020
