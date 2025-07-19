# Django Admin Interface Setup for Book Model

## Register Book Model

In `bookshelf/admin.py`:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
