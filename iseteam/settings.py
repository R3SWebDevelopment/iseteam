import os, sys
import dj_database_url

TEMPLATE_CONTEXT_PROCESSORS = (
    'django_facebook.context_processors.facebook',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

gettext_noop = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Juan Carlos Cayetano', 'jc@brainn.co'),
)

AUTH_PROFILE_MODULE = 'profile.Profile'

MANAGERS = ADMINS

#import dj_database_url   # use this to setup in localsettings.
DATABASES = {'default':
                   dj_database_url.config(
                  default='postgres://wesaqcqdkycbqp:SuyLbZne6yoAQAtWIDNRwWRoG5@ec2-23-23-81-221.compute-1.amazonaws.com:5432/d6mpu8c00tulqs')
        }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-MX'

LANGUAGES = (

('es-mx', gettext_noop('Mexican Spanish')),

)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#Site Root
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

#AMAZON
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJBJPT42ROYJRYKFA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'isemonterrey'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#AMAZON

#FILES
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
#FILES

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z-=!)pets3$zg01_#5nr7v7h50avn&amp;s8i+t2u*numd_mvp=hb_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'iseteam.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'iseteam.wsgi.application'

TEMPLATE_DIRS = ( os.path.join(SITE_ROOT, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'gunicorn',
    'storages',

    'iseteam.airport',
    'iseteam.buddies',
    'iseteam.contact',
    'iseteam.events',
    'iseteam.local',
    'iseteam.parties',
    'iseteam.pictures',
    'iseteam.profile',
    'iseteam.staff',
    'iseteam.trips',
    'iseteam.housing',
    'iseteam.gallery',
    'iseteam.admin',
    'autoslug',
    'django_facebook',
    'stripe',

)


STRIPE_LIVE_SECRET = 'sk_live_XOMUNDwrgaXj92tYGIYkjLS7'
STRIPE_LIVE_PUBLISHABLE = 'pk_live_JARW2mXGPwjTIB536icUv3R0'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#Facebook Settings
FACEBOOK_APP_ID = '433672563407144'
FACEBOOK_APP_SECRET = 'c38f1db10f466a8133601cca915284dc'

#Multiuploader Settings
MULTI_FILE_DELETE_URL = 'multi_delete'
MULTI_IMAGE_URL = 'multi_image'
MULTI_IMAGES_FOLDER = 'multiuploader_images'

#EMAIL
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app16346380@heroku.com'
EMAIL_HOST_PASSWORD = 'sazpesm74171'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@isefamily.com'

STAFF_EMAIL = ('info@isefamily.com',)

LOGIN_REDIRECT_URL = '/admin/trips/all-trips/'

SITE_URL = 'https://www.isefamily.com'



