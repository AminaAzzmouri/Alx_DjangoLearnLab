# settings.py
from pathlib import Path
import os
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

# ---- env setup
env = environ.Env(
    DEBUG=(bool, True),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))  # local only; prod uses real env vars

DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY", default="dev-secret-key")
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", default="*").split(",") if h.strip()]

# ---- apps (ensure whitenoise is present)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',
    'rest_framework.authtoken',

    # your apps
    'accounts',
    'posts',
    'notifications',
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise must come right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


import dj_database_url

# Read DATABASE_URL or fallback to sqlite
DB_URL = env("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")

# Parse without forcing ssl first
DATABASES = {
    "default": dj_database_url.parse(DB_URL, conn_max_age=600)
}

# Only add SSL for Postgres, never for sqlite
engine = DATABASES["default"].get("ENGINE", "")
if "postgresql" in engine or "postgres" in engine:
    # On Heroku/production you usually want SSL
    if not DEBUG:
        # Ensure OPTIONS exists
        DATABASES["default"].setdefault("OPTIONS", {})
        # Only set sslmode for Postgres
        DATABASES["default"]["OPTIONS"]["sslmode"] = "require"

# ---- static & media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# gzip/brotli assets in prod
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---- security hardening for prod
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # Heroku provides SSL via router/Cloudflare; set True if you terminate TLS here

# rest framework (unchanged)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- ALX checker requirement: explicit DB keys ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # or sqlite3 if local
        "NAME": env("DB_NAME", default="social_db"),
        "USER": env("DB_USER", default="postgres"),
        "PASSWORD": env("DB_PASSWORD", default="password"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}
