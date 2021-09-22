"""
Django settings for menu project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from django.contrib import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&)^s$n00)rao6l=sitobp$wm#(sqnikfl@3my91uw(ygv35jds'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost","127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    "social_django",
    "ckeditor",
    "ckeditor_uploader",
    "captcha",
    "bootstrap4",
    'django_cleanup',
    'easy_thumbnails',
    "icon.apps.IconConfig",
    'rest_framework',
    'corsheaders',
]

SESSION_ENGINE =  "django.contrib.sessions.backends.cache"
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
MESSAGE_LEVEL = messages.DEBUG
CRITICAL = 50
MESSAGE_TAGS = {
    CRITICAL:"critical"
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        "core.middleware.ExceptionMiddleware",

]

ROOT_URLCONF = 'menu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'menu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        
        'file': {
            'format': '%(asctime)s  %(name)-12s %(levelname)-8s <--> %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/home/yaroslav/Python/Django/menu/logging/log.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['file']
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        "OPTIONS":{
            "max_similarity" : 0.7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': "core.validators.NoForbiddenValidator" ,
        "OPTIONS": {
            "forbidden_list": (f"'-/+/=/./,/'" )
        }
    },
    {
        'NAME': 'core.validators.ConsistUppercaseValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
    )
# STATIC_ROOT = os.path.join(BASE_DIR, "assets")


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

ADMINS = [('Me', 'djangocommunitypython@gmail.com'), ]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# SERVER_EMAIL = 'duhanov2003@gmail.com'
EMAIL_PORT = 587
# DEFAULT_FROM_EMAIL = 'duhanov2003@gmail.com'
EMAIL_HOST_USER = 'duhanov2003@gmail.com'
EMAIL_HOST_PASSWORD = '31032003uaroslav'
EMAIL_USE_TLS = True


SOCIAL_AUTH_POSTGRES_JSONFIELD = True

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)



SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "796246915455-u9o08oa749tlgd2o126eq0v884oju2r7.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "Qt18SdY9IUcL10X8MGLwMp3r"


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, "menu_cache"),
    }
}


# ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        'skin': 'moono-dark',
    }
}   

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_IMAGE_SIZE = (130,75)
CAPTCHA_MATH_CHALLENGE_OPERATOR = "x"
САРТСНА_LETTER_ROТAТION = (0,0)
САРТСНА_BACKGROUND_COLOR = "#000000" 
САРТСНА_FOREGROUND_COLOR = "#bbcc"


THUМВNAIL_ALIASES = {
    '': {
        'default': {
            'size': (500, 300),
            'crop': 'scale',
            "bw": True, 
        }, 
    },       
}


ADMIN = [
    ('Yaryk', 'duhanov2003@gmail.com'),
    ('Admin2', 'admin2@othersite.com'),
    ('MegaAdmin', 'megaadmin@megasite.com')
]