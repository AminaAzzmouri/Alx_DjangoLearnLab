# Django Models Project — relationship_app

This Django project demonstrates advanced model relationships using Django's ORM.  
It showcases the use of **ForeignKey**, **ManyToManyField**, and **OneToOneField** relationships through a simple library management example.

## Project Structure

- `relationship_app/models.py` — Defines four models with complex relationships:
  - **Author**: Represents authors.
  - **Book**: Each book has a ForeignKey to an Author.
  - **Library**: Each library contains many books (ManyToManyField).
  - **Librarian**: One librarian per library (OneToOneField).

- `relationship_app/query_samples.py` — Contains example query functions to:
  - Retrieve all books by a specific author.
  - List all books in a library.
  - Get the librarian assigned to a library.

## Setup & Usage

1. Clone the repository and navigate to the project directory.
2. Ensure the app `relationship_app` is added to `INSTALLED_APPS` in `settings.py`.
3. Run migrations:
    ```bash
    python manage.py makemigrations relationship_app
    python manage.py migrate
    ```
4. Use the Django shell or run `query_samples.py` to test the queries.

## Example Queries

```python
from relationship_app.query_samples import query_all_books_by_author, query_all_books_in_library, query_librarian_for_library

books_by_author = query_all_books_by_author("J.K. Rowling")
books_in_library = query_all_books_in_library("Central Library")
librarian = query_librarian_for_library("Central Library")
