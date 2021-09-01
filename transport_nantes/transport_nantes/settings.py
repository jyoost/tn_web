"""
Django settings for transport_nantes project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from . import settings_local

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_local.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings_local.DEBUG
ROLE = settings_local.ROLE

ALLOWED_HOSTS = settings_local.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'surveys.apps.SurveysConfig',
    'asso_tn.apps.AssoTnConfig',
    'mailing_list.apps.MailingListConfig',
    'velopolitain_observatoire.apps.VelopolitainObservatoireConfig',
    'clickcollect.apps.ClickCollectConfig',
    'authentication.apps.AuthenticationConfig',
    'topicblog.apps.TopicBlogConfig',
    'dashboard.apps.DashboardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'geoplan',
    'stripe_app',
    'crispy_forms',
    'django_countries',
] + settings_local.MORE_INSTALLED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'asso_tn.middleware.default_context.DefaultContextMiddleware',
]

ROOT_URLCONF = 'transport_nantes.urls'

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
                'asso_tn.context_processors.role',
                'django.template.context_processors.media'
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = settings_local.DATABASES

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
PASSWORD_RESET_TIMEOUT_DAYS = 1

EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
AWS_ACCESS_KEY_ID = settings_local.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings_local.AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION = settings_local.AWS_DEFAULT_REGION
DEFAULT_FROM_EMAIL = settings_local.DEFAULT_FROM_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        #'mail_admins': {
        #    'level': 'ERROR',
        #    'filters': ['require_debug_false'],
        #    'class': 'django.utils.log.AdminEmailHandler'
        #},
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': settings_local.LOG_DIR + "tn_web.log",
            'formatter': 'django.server',
        }
    },
    'loggers': {
        'app': {
            # 'handlers': ['console', 'mail_admins'],
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            # 'handlers': ['console', 'mail_admins'],
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True
# TODO: stay on same page if authorised to do so.
LOGIN_REDIRECT_URL = 'index'
#LOGOUT_REDIRECT_URL = 'index'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = settings_local.STATIC_URL
STATIC_ROOT = settings_local.STATIC_ROOT

# Prefix for uploaded files. Must be different from static_url
MEDIA_URL = settings_local.MEDIA_URL
# Directory where uploaded files are stored
MEDIA_ROOT = settings_local.MEDIA_ROOT

# Define this for nginx contexts.
if 'STATIC_ROOT' in dir(settings_local):
    STATIC_ROOT = settings_local.STATIC_ROOT

# CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)
## I have a low success rate on the captcha with noise_arcs enabled.
## (This is the default behaviour.)
# CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs','captcha.helpers.noise_dots',)
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_LENGTH = 5

STRIPE_PUBLISHABLE_KEY = settings_local.STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY = settings_local.STRIPE_SECRET_KEY
STRIPE_ENDPOINT_SECRET = settings_local.STRIPE_ENDPOINT_SECRET
