# Django Blog Project

A simple, responsive Django blog application with user registration, login, and blog post pages. This project demonstrates the use of Django templates, static files (CSS & JS), and responsive design.

---

## Features

- **Homepage** – A welcoming landing page.
- **User Registration** – Secure registration form with CSRF protection.
- **User Login** – Login page with placeholders for username/email and password.
- **Blog Posts** – Page displaying all blog posts (currently static content).
- **Responsive Design** – Works well on desktop and mobile devices.
- **Enhanced UI/UX** – Modern form styles, hover effects, and animated buttons.

---

## Project Structure

django_blog/
├── blog/
│ ├── templates/
│ │ └── blog/
│ │ ├── base.html
│ │ ├── home.html
│ │ ├── login.html
│ │ ├── register.html
│ │ └── posts.html
│ ├── static/
│ │ ├── css/
│ │ │ └── styles.css
│ │ └── js/
│ │ └── scripts.js
│ ├── views.py
│ ├── urls.py
│ └── models.py
├── manage.py
└── db.sqlite3


---

## Installation

1. **Clone the repository:**

git clone https://github.com/yourusername/django-blog.git
cd django-blog


2.  Create and activate a virtual environment:
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


3.  Install dependencies:
pip install django==3.2.25


4. Apply migrations:
python manage.py migrate


5. Run the server:
python manage.py runserver



** Usage:

Navigate to Home, Blog Posts, Register, or Login using the top navigation menu.

Registration and login forms are ready for future integration with Django’s authentication system.

Blog posts page currently displays static content but can be extended to dynamic posts.


** Static Files & Templates

CSS – static/css/styles.css contains all the styling for header, footer, forms, buttons, and animations.

JS – static/js/scripts.js handles basic dynamic behaviors.

Templates – templates/blog/ contains all HTML templates extending base.html.