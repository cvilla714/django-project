import os
import boto3
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (in case you need any fallback)
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# Function to get secret from AWS Secrets Manager
def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

# Fetch the secret from AWS Secrets Manager
SECRET_NAME = "dev-django-project-rds-credentials"  # Replace with your actual secret name
secrets = get_secret(SECRET_NAME)

# Set the Django settings using values from AWS Secrets Manager
SECRET_KEY = secrets.get("SECRET_KEY")
DEBUG = secrets.get("DEBUG", 'False') == 'True'
DB_NAME = secrets.get("DB_NAME")
DB_USER = secrets.get("DB_USER")
DB_PASSWORD = secrets.get("DB_PASSWORD")
DB_HOST = secrets.get("DB_HOST")
DB_PORT = secrets.get("DB_PORT", "5432")

# AWS Credentials
AWS_ACCESS_KEY_ID = secrets.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = secrets.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = secrets.get("AWS_STORAGE_BUCKET_NAME")

# Debug print statements (optional, for testing)
print(f"Loaded DB_HOST: {DB_HOST}")
print(f"Loaded AWS_STORAGE_BUCKET_NAME: {AWS_STORAGE_BUCKET_NAME}")

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "corsheaders",
    "backend.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

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

WSGI_APPLICATION = "backend.wsgi.application"

# GraphQL & JWT settings
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHENE = {
    'SCHEMA': 'backend.api.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

# PostgreSQL database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# AWS S3 for file storage (Using the folder you specified 'rdsdjango')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/rdsdjango'
AWS_DEFAULT_ACL = None

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Password validators
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

# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media settings
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
