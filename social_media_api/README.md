# Social Media API — Auth Bootstrap

This is the foundational backend (Django + DRF) for a Social Media API with a custom user and token authentication.

## Stack
- Django
- Django REST Framework
- DRF Token Authentication

## Setup

python -m venv .venv
# Windows: .venv\Scripts\activate
pip install django djangorestframework
django-admin startproject social_media_api
cd social_media_api
python manage.py startapp accounts
# Add 'rest_framework', 'rest_framework.authtoken', 'accounts' to INSTALLED_APPS
# Set AUTH_USER_MODEL = 'accounts.User'
python manage.py makemigrations && python manage.py migrate
python manage.py runserver


## Posts & Comments API

### Posts
- `GET /api/posts/` — list (search `?search=term`, order `?ordering=-created_at`)
- `POST /api/posts/` — create (auth)
- `GET /api/posts/{id}/` — retrieve
- `PUT/PATCH /api/posts/{id}/` — update (owner only)
- `DELETE /api/posts/{id}/` — delete (owner only)

Body (create/update):

{ "title": "Hello", "content": "..." }

Comments

GET /api/comments/ — list

POST /api/comments/ — create (auth)

GET /api/comments/{id}/ — retrieve

PUT/PATCH /api/comments/{id}/ — update (owner only)

DELETE /api/comments/{id}/ — delete (owner only)

Body (create):

{ "post": 1, "content": "Great!" }




## Follows & Feed

### Follow Management
- `POST /api/accounts/follow/<user_id>/` — follow a user (auth)
- `POST /api/accounts/unfollow/<user_id>/` — unfollow a user (auth)

### Feed
- `GET /api/feed/` — posts from users I follow (auth), ordered by newest first

### Notes
- User model adds:
  ```py
  following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

Only the authenticated user can modify their own following list.



POST /api/posts/{pk}/like/ — like a post (auth)

POST /api/posts/{pk}/unlike/ — unlike a post (auth)

GET /api/notifications/ — list (auth), newest first, shows unread/read

PATCH /api/notifications/{pk}/read/ — mark read (auth)

Notifications created on:

follow (followed you)

like (liked your post)

comment (commented on your post)