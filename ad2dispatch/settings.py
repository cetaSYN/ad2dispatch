import os

DOMAIN = os.environ.get('AD2_DOMAIN')

# Organization Name
ORG_NAME = os.environ.get('AD2_ORG_NAME')
# Organization Acronym
ORG_ACRONYM = os.environ.get('AD2_ORG_ACRONYM')
# Organization Phone Number: please use international format. (+12345678900)
ORG_PHONE = os.environ.get('AD2_ORG_PHONE')
# Organization Phone Number: friendly format.
ORG_PHONE_DISPLAY = os.environ.get('AD2_ORG_PHONE_DISPLAY')
# Alternate Organization Phone Number: please use international format.
ORG_PHONE_ALT = os.environ.get('AD2_ORG_PHONE_ALT')
# Alternate Organization Phone Number: friendly format.
ORG_PHONE_ALT_DISPLAY = os.environ.get('AD2_ORG_PHONE_ALT_DISPLAY')
# Disclaimer [Required by most *ADD orgs]
DISCLAIMER = os.environ.get('AD2_ORG_DISCLAIMER', '''AS REQUIRED BY AFI 34-223
WE ARE REQUIRED TO INFORM YOU THIS IS A PRIVATE ORGANIZATION.
 IT IS NOT A PART OF THE DEPARTMENT OF DEFENSE OR ANY OF ITS COMPONENTS AND IT
HAS NO GOVERNMENTAL STATUS.''')

# Social links
# Use just the name with no markup.
# Ex: OffuttADD, not @OffuttADD, and not a URL.
FACEBOOK = os.environ.get('AD2_ORG_FACEBOOK')
TWITTER = os.environ.get('AD2_ORG_TWITTER')

# Google Maps API key
# https://developers.google.com/maps/documentation/javascript/get-api-key
MAPS_KEY = os.environ.get('AD2_MAPS_KEY', '')

# Time zone
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = os.environ.get('AD2_TIMEZONE', 'America/Chicago')

# !!**!! SECURITY WARNING: keep the secret key used in production secret !!**!!
# Security Key
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ.get('AD2_SECRET_KEY')

DEBUG = os.environ.get('AD2_DEBUG').lower() == 'true'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = os.environ.get('AD2_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'userprofiles',
    'news',
    'pages',
    'events',
    'zappa_django_utils'
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'ad2dispatch.urls'

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
                'ad2dispatch.context_processors.org_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'ad2dispatch.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('AD2_DB_HOST'),
        'NAME': os.environ.get('AD2_DB_NAME', 'ad2dispatch'),
        'USER': os.environ.get('AD2_DB_USER', 'ad2dispatch'),
        'PASSWORD': os.environ.get('AD2_DB_PASSWORD'),
        'PORT': os.environ.get('AD2_DB_PORT', '3306'),
        'OPTIONS': {'ssl':{
                    'key':'./client-key.pem',
                    'cert':'./client-cert.pem',
                    'ca':'./ca.pem'
                    }
        }
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'NumericPasswordValidator',
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp'
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
WHITENOISE_STATIC_PREFIX = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

AXES_LOGIN_FAILURE_LIMIT = 4
AXES_COOLOFF_TIME = 1
AXES_CACHE = 'axes_cache'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_HTML = False
REGISTRATION_AUTO_LOGIN = True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 465
# EMAIL_HOST = os.environ.get('AD2_EMAIL_HOST')
# EMAIL_HOST_PASSWORD = os.environ.get('AD2_EMAIL_PASSWORD')
# EMAIL_HOST_USER = os.environ.get('AD2_EMAIL_USER')

EMAIL_SUBJECT_PREFIX = ORG_ACRONYM
EMAIL_USE_LOCALTIME = True
DEFAULT_FROM_EMAIL = "noreply@{}".format(DOMAIN)
SERVER_EMAIL = "alert@{}".format(DOMAIN)

# SES-backed email
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')

AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME')
AWS_SES_REGION_ENDPOINT = \
   "email.{}.amazonaws.com".format(AWS_SES_REGION_NAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
