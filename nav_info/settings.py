import os
from os import environ
from django.urls import reverse_lazy


def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = SECRET_KEY = get_env(
    'SECRET_KEY', 'b13r*3jp1y37p9tjvqc=j_(q=kddn1!n#9+jk1tjj7b@_(6**k')

DEBUG = get_env('DEBUG', True)

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
]

LOCAL_APPS = [
    'user_profile.apps.UserProfileConfig',
    'soap_client',
]

if DEBUG:
    # Silk
    THIRD_PARTY_APPS = ['silk', ] + THIRD_PARTY_APPS

    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True
    SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, 'silk')
    SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
    SILKY_MAX_RESPONSE_BODY_SIZE = -1
    SILKY_META = True

    # drf-generators
    THIRD_PARTY_APPS = THIRD_PARTY_APPS + ['drf_generators', ]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = ['silk.middleware.SilkyMiddleware', ] + MIDDLEWARE

ROOT_URLCONF = 'nav_info.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'nav_info.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('POSTGRES_DB', 'postgres_db'),
        'USER': get_env('POSTGRES_USER', 'postgresuser'),
        'PASSWORD': get_env('POSTGRES_PASSWORD', 'mysecretpass'),
        'HOST': get_env('POSTGRES_HOST', 'localhost'),
        'PORT': 5432
    }
}

AUTH_USER_MODEL = 'user_profile.UserProfile'

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


LANGUAGE_CODE = get_env('LANGUAGE_CODE', 'en-us')

TIME_ZONE = get_env('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,

}

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
