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
