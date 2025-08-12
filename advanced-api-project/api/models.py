from django.db import models
from django.utils import timezone

# Author model - represents a book's author
class Author(models.Model):
    name = models.CharField(max_length=255)  # Author's name

    def __str__(self):
        return self.name


# Book model - represents a single book by an author
class Book(models.Model):
    title = models.CharField(max_length=255)  # Book title
    publication_year = models.IntegerField()  # Year published
    author = models.ForeignKey(
        Author,
        related_name='books',  # Enables reverse lookup: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
