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

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'noreply@buythebay.com'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'noreply@buythebay.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

PAYPAL_SERVER = 'https://api-3t.sandbox.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.sandbox.paypal.com/webscr'
PAYPAL_USER = 'merch_1281066320_biz_api1.gmail.com'
PAYPAL_PASS = '1281066328'
PAYPAL_SIGNATURE = 'AP5ErZnuVaoE-u3JZQnMRJXRlcHnA-KyqL7eaN1CbAp5nWvcGzwLwPWT'

FACEBOOK_APP_ID = '159956577356734'
FACEBOOK_API_KEY = '7e7dfc67cce994c31942d05030e9b8ae'
FACEBOOK_SECRET_KEY = 'cc9160516db0f30f0f266a3b647c69cf'

TWITTER_API_KEY = '0XCtgCwTPsfPdTHFZy1w'
TWITTER_SECRET = 'twGByj00hd0Rxg4rn7gyENTfT5bobvvPFK3p8bflp0o'

BITLY_LOGIN = 'philosophie'
BITLY_API_KEY = 'R_2e5a07bcbd10741541f6e54aa25312ed'
