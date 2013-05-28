import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_DATE = ("Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez")

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = os.path.abspath('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.abspath('efforia/public'),]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    ('efforia.jade.ext.django.Loader',(
    	'django.template.loaders.filesystem.Loader',
    	'django.template.loaders.app_directories.Loader',
    )),
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'efforia.wsgi.application'
TEMPLATE_DIRS = (
    os.path.abspath('static'),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'efforia',
    'efforia.bootstrap',
    'django.contrib.admin',
    'efforia.paypal',
    'efforia.pagseguro',
    'efforia.infinite',
    'gunicorn',
    'south'
]

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

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'efforia.Profile'
