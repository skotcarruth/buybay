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

# Paypal Express Checkout (lame)
PAYPAL_SERVER = 'https://api-3t.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.paypal.com/cgi-bin/webscr.'
PAYPAL_USER = 'nburdick_api1.healthebay.org'
PAYPAL_PASS = 'BPFL5JQREGCNZ4KL'
PAYPAL_SIGNATURE = 'AkrturaUrjwo1xbii9WwCzlYDWEDA2iWs3FpjP-5TZ0vH3VWMB6nlgwM'

# Paypal Web Standard Payments (less lame)
PAYPAL_CURRENCY_CODE = 'USD'
PAYPAL_POST_URL = 'https://www.paypal.com/cgi-bin/webscr'
# PAYPAL_BUSINESS = 'buythebaydev@gmail.com'

FACEBOOK_APP_ID = '159956577356734'
FACEBOOK_API_KEY = '7e7dfc67cce994c31942d05030e9b8ae'
FACEBOOK_SECRET_KEY = 'cc9160516db0f30f0f266a3b647c69cf'

TWITTER_API_KEY = '0XCtgCwTPsfPdTHFZy1w'
TWITTER_SECRET = 'twGByj00hd0Rxg4rn7gyENTfT5bobvvPFK3p8bflp0o'

BITLY_LOGIN = 'philosophie'
BITLY_API_KEY = 'R_2e5a07bcbd10741541f6e54aa25312ed'
