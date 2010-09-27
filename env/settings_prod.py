# Settings overrides for the prod environment

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'buybay',
        'USER': 'www',
        'PASSWORD': 'buybay',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

PAYPAL_SERVER = 'https://api-3t.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.paypal.com/webscr'
