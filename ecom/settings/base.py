import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY =  os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRDPARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
]

LOCAL_APPS = [
    "app_modules.users",
    "app_modules.products",
    "app_modules.orders",
]

INSTALLED_APPS = LOCAL_APPS + THIRDPARTY_APPS + DJANGO_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ecom.middleware.customer_middlewares.DebuggingMiddleware',
    'ecom.middleware.customer_middlewares.CompressionMiddleware',
    'ecom.middleware.customer_middlewares.DatabaseQueryLoggingMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

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

WSGI_APPLICATION = 'ecom.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":  os.environ.get("DATABASE_NAME"),
        "USER":  os.environ.get("DATABASE_USER"),
        "PASSWORD":  os.environ.get("DATABASE_PASSWORD"),
        "HOST":  os.environ.get("DATABASE_HOST"),
        "PORT":  os.environ.get("DATABASE_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.Users"

SUPER_USER = {
    "ADMIN_EMAIL": os.environ.get("ADMIN_EMAIL"),
    "ADMIN_USERNAME": os.environ.get("ADMIN_USERNAME"),
    "ADMIN_PASSWORD": os.environ.get("ADMIN_PASSWORD"),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "EXCEPTION_HANDLER": "app_modules.base.exception.handle_exception",
    "DEFAULT_RENDERER_CLASSES": ["app_modules.base.renderers.BaseJSONRenderer"],
    "DEFAULT_PAGINATION_CLASS": "app_modules.base.pagination.CustomPagination",
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),    
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7), 
    'BLACKLIST_AFTER_ROTATION': True,
}

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
}