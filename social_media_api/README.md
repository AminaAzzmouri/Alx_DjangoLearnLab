# Social Media API — Auth Bootstrap

This is the foundational backend (Django + DRF) for a Social Media API with a custom user and token authentication.

## Stack
- Django
- Django REST Framework
- DRF Token Authentication

## Setup
```bash
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
