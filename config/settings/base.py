"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import (
    default_headers,
)
from environ import Env
from command_scheduler.enums import ScheduleType
from command_scheduler.utils import args


SITE_ID = 1

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SILENCED_SYSTEM_CHECKS = ["rest_framework.W001"]

ENV_FILE = ".env"
Env.read_env(BASE_DIR / ENV_FILE)
env = Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "django_filters",
    "django_extensions",
    "colorfield",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "drf_standardized_response",
    "drf_standardized_errors",
    "drf_pagination_meta_wrap",
]

LOCAL_APPS = [
    "command_scheduler",
    "ranker.common",
    "ranker.authentication",
    "ranker.accounts",
    "ranker.users",
    "ranker.recent_searches",
    "ranker.level_titles",
    "ranker.difficulties",
    "ranker.challenges",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Mail
DEFAULT_FROM_EMAIL = "ranker.noreply@gmail.com"

# User Model
AUTH_USER_MODEL = "users.UserModel"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"


# Log
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        #         "db_query": {
        #             "level": "DEBUG",
        #             "class": "logging.FileHandler",
        #             "filename": "tmp/logs/db_queries.log",
        #         },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "X-Session-Token",
    "location",
)

# Rest Framework
REST_FRAMEWORK = {
    # API Versioning
    "DEFAULT_VERSION": "v1",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    # Exception
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    # Response
    "DEFAULT_RENDERER_CLASSES": (
        "drf_standardized_response.renderers.StandardizedJSONRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "ranker.authentication.authentication.UsernameAuthentication",
    ],
    # Pagination
    "PAGE_SIZE": 15,
    # Test
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    # Docs
    "DEFAULT_SCHEMA_CLASS": "ranker.docs.openapi.AutoSchema",
}

# Api Docs
SPECTACULAR_SETTINGS = {
    "TITLE": "Rapid Task",
    "DESCRIPTION": "The api documentation of Rapid Task API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
    },
    "POSTPROCESSING_HOOKS": (
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
    ),
}


# Command Scheduler

SCHEDULED_COMMANDS = [
    {
        "enabled": True,
        "schedule": ScheduleType.DAILY,
        "command": "update_ranking",
        "args": args(chunk=1000),
    },
    {
        "enabled": True,
        "schedule": ScheduleType.DAILY,
        "command": "reset_repeated_challenges",
        "args": args("D", chunk=1000),
    },
    {
        "enabled": True,
        "schedule": ScheduleType.WEEKLY,
        "task": "reset_repeated_challenges",
        "args": ["W"],
        "args": args("W", chunk=1000),
    },
    {
        "enabled": True,
        "schedule": ScheduleType.MONTHLY,
        "task": "reset_repeated_challenges",
        "args": args("M", chunk=1000),
    },
]

# Ranker

# ranker.authentication
TOKEN_LOGIN_SALT = env("TOKEN_LOGIN_SALT")
LOGIN_TOKEN_MAX_AGE = 5  # seconds

# ranker.common
GROQ_API_KEY = env("GROQ_API_KEY")

# ranker.users
USERNAME_MAX_LENGTH = 35
USERNAME_MAX_SUGGESTIONS = 3
USERNAME_GENERATION_MAX_ATTEMPTS = 10

XP_PER_LEVEL = 1000
