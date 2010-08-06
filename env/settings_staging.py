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
DEFAULT_FROM_EMAIL = 'noreply@buythebay.jeffschenck.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

PAYPAL_SERVER = 'https://api-3t.sandbox.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.sandbox.paypal.com/webscr'
PAYPAL_USER = 'merch_1281066320_biz_api1.gmail.com'
PAYPAL_PASS = '1281066328'
PAYPAL_SIGNATURE = 'AP5ErZnuVaoE-u3JZQnMRJXRlcHnA-KyqL7eaN1CbAp5nWvcGzwLwPWT'
