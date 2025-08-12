# Advanced API Project — Book Endpoints

This project provides CRUD operations for books using Django REST Framework’s generic views.

## Endpoints

| Method | Endpoint                 | Description | Auth Required |
|--------|--------------------------|-------------|--------------|
| GET    | /api/books/              | List all books (supports `year` and `author_id` filters) | No |
| GET    | /api/books/<id>/         | Retrieve book details | No |
| POST   | /api/books/create/       | Create a new book | Yes |
| PUT    | /api/books/<id>/update/  | Update all details of a book | Yes |
| PATCH  | /api/books/<id>/update/  | Update specific details of a book | Yes |
| DELETE | /api/books/<id>/delete/  | Delete a book | Yes |

## Permissions
- Read (GET) requests are available to everyone.
- Write (POST, PUT, PATCH, DELETE) requests require authentication.

## Filters
- `?year=YYYY` — Filters books by publication year.
- `?author_id=N` — Filters books by author.

Example:


GET /api/books/?year=2020
GET /api/books/?author_id=1




## API Filtering, Searching, and Ordering

The **BookListView** now supports advanced querying.

### Filtering
Filter by:
- `title`
- `author`
- `publication_year`

Example:
