from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone


"""
This file defines serializers for converting model instances into JSON and vice versa.

We have two serializers:
1. BookSerializer — serializes Book objects, including validation for publication year.
2. AuthorSerializer — serializes Author objects and includes a nested list of related books.

Relationship Handling in Serializers:
- The Book model has a ForeignKey to Author, meaning each book is linked to one author.
- In AuthorSerializer, we include a nested BookSerializer to show all books written by that author.
- The related_name='books' in the Book model makes it possible to easily access an author's books
  as author.books.all(), which is then serialized using BookSerializer.
"""


class BookSerializer(serializers.ModelSerializer):
    
      """
    Serializer for the Book model.

    Purpose:
    - Convert Book model instances into JSON for API responses.
    - Convert incoming JSON data into Book model instances for API requests.
    - Perform validation before saving data to the database.

    Fields:
    - All model fields ('title', 'publication_year', 'author') are included.

    Validation:
    - Custom validation ensures the publication year is not set in the future.
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # All fields: title, publication_year, author

    
    def validate_publication_year(self, value):
        
         """
        Check that the publication year is not greater than the current year.

        Args:
        - value (int): The publication year provided by the user.

        Returns:
        - value if valid.

        Raises:
        - serializers.ValidationError: If the year is in the future.
        """
        
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future (current year: {current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    
   """
    Serializer for the Author model.

    Purpose:
    - Convert Author model instances into JSON.
    - Include a nested representation of the author's books.

    Nested Serializer:
    - 'books' is a read-only field that uses BookSerializer to serialize each book.
    - 'many=True' tells DRF that the author may have multiple books.
    - read_only=True ensures that books cannot be created directly via AuthorSerializer.

    Fields:
    - 'name' — the author's name.
    - 'books' — list of books written by this author, serialized using BookSerializer.
    """
    
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
