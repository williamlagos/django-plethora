import os

DEBUG = True
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
STATICFILES_DIRS = [os.path.abspath('plethora/public'),]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'plethora/public' ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('pypugjs.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
            'builtins': ['pypugjs.ext.django.templatetags'],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'plethora.urls'
WSGI_APPLICATION = 'plethora.wsgi.application'

INSTALLED_APPS = [
    'flat_responsive',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_pagseguro',
    'pure_pagination',
    'socialize',
    'shipping',
    'feedly',
    'django_distill',
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
AUTH_PROFILE_MODULE = 'socialize.Profile'

EFFORIA_APPS = ()
EFFORIA_OBJS = {}
EFFORIA_NAMES = {}
EFFORIA_TOKENS = {}

ADMINS = (('William Oliveira de Lagos', 'william@efforia.com.br'),)
MANAGERS = ADMINS
SECRET_KEY = 'x5dvfbk$u-(07^f1229p*_%rcuc+nka45j6awo==*jkyjiucql'

#DATABASES = {
#  'default': {
#    'ENGINE': 'django.db.backends.postgresql_psycopg2',
#    'NAME': 'd6i6a0klirtqjd',
#    'HOST': 'ec2-54-243-243-176.compute-1.amazonaws.com',
#    'PORT': 5432,
#    'USER': 'kkoaphemdgvutt',
#    'PASSWORD': 'ztTIw8EcIYX2UlNolrVmTb8yZQ'
#  }
#}

DATABASES = {
  'default': {
     'ENGINE':'django.db.backends.sqlite3',
     'NAME':'plethora.db'
   }
}

#EFFORIA_APPS = ('spread','promote')
EFFORIA_ACTIONS = {'plethora':[]}
EFFORIA_APPS = ('plethora',)
EFFORIA_OBJS.update({
    'plethora':  ['Playable','Spreadable','Image','Product'],
#    'promote': ['Project','Event']
})
EFFORIA_NAMES.update({
    'plethora':  ('Espalhe','spread'),
#    'promote': ('Promova','promote')
})
EFFORIA_TOKENS.update({
    "@": "Profile",
#    "#": "Project",
#    "@#":"Project",
#    "##":"Movement",
    ">": "Playable",
    ">!":"Playable",
    "!": "Spreadable",
    "!!":"Spreadable",
#    "@!":"Event",
#    "@": "Event",
#    "@@":"Event",
    "%": "Image",
    "%!":"Image",
    "!#":"Page",
    "!%":"Image",
    "$$":"Product"
})
INSTALLED_APPS.extend(EFFORIA_APPS)
STATICFILES_DIRS.extend((
    os.path.abspath('plethora/public'),
#    os.path.abspath('promote/public'),
))


PAYPAL_RECEIVER_EMAIL = 'caokzu@gmail.com'
PAYPAL_NOTIFY_URL = '/paypal'
PAYPAL_RETURN_URL = '/'
PAYPAL_CANCEL_RETURN = '/cancel'

PAGSEGURO_EMAIL_COBRANCA = 'contato@efforia.com.br'
PAGSEGURO_TOKEN = '1a3ea7wq2e7eq8e1e223add23ad23'
PAGSEGURO_URL_RETORNO = '/pagseguro/retorno/'
PAGSEGURO_URL_FINAL = '/obrigado/'
PAGSEGURO_ERRO_LOG  = '/tmp/pagseguro_erro.log'

ALLOWED_HOSTS = ['*',]
