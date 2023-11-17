import os
from pathlib import Path
from configurations import Configuration
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env_file_path = os.path.join(BASE_DIR, 'currency_conversion_api.env')
if os.path.exists(env_file_path):
    print("Using API env file")
    environ.Env.read_env(env_file_path)
USE_HTTPS = env.bool("USE_HTTPS", default=False)


class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = get_random_secret_key()

    DEBUG = True

    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

    # Cors Setup
    cors_hosts = env.list("CORS_HOSTS", default=[])
    if cors_hosts:
        CORS_ALLOW_ALL_ORIGINS = False
        CORS_ALLOWED_ORIGINS = cors_hosts
    else:
        CORS_ALLOW_ALL_ORIGINS = True

    # Csrf Setup
    csrf_hosts = env.list("CSRF_HOSTS", default=[])
    if csrf_hosts:
        CSRF_TRUSTED_ORIGINS = csrf_hosts

    # X Frame Setup
    X_FRAME_OPTIONS = 'DENY'

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Cors:
        "corsheaders",
        # Rest framework:
        'rest_framework',
        'django_filters',
        # Schedule jobs:
        'django_apscheduler',
        # Swager:
        'drf_yasg',
        # Custom apps:
        'core',
        'conversion_client',
        'currency',
        'api_key'
    ]

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'core.urls'

    CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

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

    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases
    DATABASES = {"default": env.db(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "default.sqlite3")
    )}

    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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

    # Internationalization
    # https://docs.djangoproject.com/en/4.1/topics/i18n/
    LANGUAGE_CODE = 'en'
    LOCALE_PATHS = [
        BASE_DIR / 'locale/',
    ]
    LANGUAGES = (
        ('en', _('English')),
        ('es', _('Spanish')),
        ("fr", _("French")),
    )
    TIME_ZONE = "UTC"
    # Enables Django’s translation system
    USE_I18N = True
    # Django will display numbers and dates using the format of the current locale
    USE_L10N = True
    # Datetimes will be timezone-aware
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/
    # (Statis url is not used in this project)
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / "static"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        }
    }

    # Django Rest Framework setting:
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "api_key.authentication.ApiKeyAuthentication"
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        #"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        #"PAGE_SIZE": 10,
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
        ],
        'EXCEPTION_HANDLER': 'core.exceptions.app_exception_handler'
    }

    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "API Key": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            },
        }
    }

    AUTH_USER_MODEL = "api_key.ApiUser"

    # Currency conversion settings

    CURRENCY_CODES = env.list("CURRENCY_CODES", default=["EUR", "USD"])
    # Maximum number of days to store a conversion
    MAX_STORED_DAYS = env.int("MAX_STORED_DAYS", default=20)
    # Maximum number of minutes to avoid updating a conversion
    MAX_NO_UPDATED_MINS = env.int("MAX_NO_UPDATED_MINS", default=5)


class Prod(Dev):
    DEBUG = False
    WSGI_APPLICATION = 'core.wsgi.application'

    # Security headers
    if USE_HTTPS:
        CSRF_COOKIE_SECURE = True
        SESSION_COOKIE_SECURE = True
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
        SECURE_SSL_REDIRECT = True
        SECURE_HSTS_SECONDS = 31536000  # 1 year
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        }
    }
