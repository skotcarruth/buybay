# Settings overrides for the staging environment
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nweave_buybay',
        'USER': 'nweave_buybay',
        'PASSWORD': 'b760573f',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'nweave_buybay'
EMAIL_HOST_PASSWORD = '0e341dd7'
DEFAULT_FROM_EMAIL = 'noreply@buythebay.org'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
