from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# ENVIRONMENT
# =========================================================

def env(key, default=None, cast=str):
    value = os.getenv(key, default)

    if cast == bool:
        return str(value).lower() in ("1", "true", "yes")

    if cast == int:
        return int(value)

    return value


DEBUG = env("DEBUG", False, bool)

SECRET_KEY = env(
    "SECRET_KEY",
    "CHANGE-ME-IN-PRODUCTION"
)

ALLOWED_HOSTS = env(
    "ALLOWED_HOSTS",
    "yourusername.pythonanywhere.com"
).split(",")


# =========================================================
# APPS
# =========================================================

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",

    # Local Apps
    "accounts",
    "academics",
    "questions",
    "progress",
    "quizzes",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    # Whitenoise for static serving
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "aspire_academy_badin.urls"

WSGI_APPLICATION = "aspire_academy_badin.wsgi.application"



# =========================================================
# DATABASE
# =========================================================
# SQLite okay for prototype.
# For production prefer PostgreSQL.

if env("USE_POSTGRES", False, bool):

    DATABASES = {
        "default": {
            "ENGINE":"django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT","5432"),
            "CONN_MAX_AGE":600,
        }
    }

else:
    DATABASES = {
        "default":{
            "ENGINE":"django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3"
        }
    }



# =========================================================
# AUTH
# =========================================================

AUTH_USER_MODEL = "accounts.Account"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]



# =========================================================
# DJANGO REST
# =========================================================

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES":(
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES":(
        "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_FILTER_BACKENDS":[
        "django_filters.rest_framework.DjangoFilterBackend"
    ],

    "DEFAULT_THROTTLE_CLASSES":[
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES":{
        "anon":"20/min",
        "user":"300/min",
    }
}



# =========================================================
# JWT
# =========================================================

SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME":
        timedelta(minutes=30),

    "REFRESH_TOKEN_LIFETIME":
        timedelta(days=7),

    "ROTATE_REFRESH_TOKENS":True,

    "BLACKLIST_AFTER_ROTATION":True,

    "AUTH_HEADER_TYPES":("Bearer",),
}



# =========================================================
# CORS / CSRF
# =========================================================

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://yourfrontend.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
]


# =========================================================
# SECURITY
# =========================================================

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

SECURE_SSL_REDIRECT = not DEBUG

SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True



# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
{
    "BACKEND":
        "django.template.backends.django.DjangoTemplates",

    "DIRS":[],

    "APP_DIRS":True,

    "OPTIONS":{
        "context_processors":[
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]
    }
}
]



# =========================================================
# STATIC / MEDIA
# =========================================================

STATIC_URL="/static/"

STATIC_ROOT=BASE_DIR / "staticfiles"

STATICFILES_DIRS=[
    BASE_DIR / "static",
]

STATICFILES_STORAGE=(
 "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR / "media"



# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE="en-us"

TIME_ZONE="UTC"

USE_I18N=True

USE_TZ=True


DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"



# =========================================================
# LOGGING
# =========================================================

LOGGING = {

"version":1,
"disable_existing_loggers":False,

"handlers":{
    "file":{
        "class":"logging.FileHandler",
        "filename":"django.log",
    },
},

"loggers":{
    "django":{
        "handlers":["file"],
        "level":"ERROR",
        "propagate":True,
    },
},
}