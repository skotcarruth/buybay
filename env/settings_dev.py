# Settings overrides for the dev environment
import os
PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'dev.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'noreply@dev.buythebay.org'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Paypal Express Checkout (lame)
PAYPAL_SERVER = 'https://api-3t.sandbox.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.sandbox.paypal.com/webscr'
PAYPAL_USER = 'merch_1281066320_biz_api1.gmail.com'
PAYPAL_PASS = '1281066328'
PAYPAL_SIGNATURE = 'AP5ErZnuVaoE-u3JZQnMRJXRlcHnA-KyqL7eaN1CbAp5nWvcGzwLwPWT'

# Paypal Web Standard Payments (less lame)
PAYPAL_CURRENCY_CODE = 'USD'
# PAYPAL_POST_URL = 'https://www.paypal.com/cgi-bin/webscr'
PAYPAL_POST_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
PAYPAL_BUSINESS = 'buythebaydev@gmail.com'

FACEBOOK_APP_ID = '132846116761716'
FACEBOOK_API_KEY = '6c600d30e9f6b4d4d6dea40f9ff04819'
FACEBOOK_SECRET_KEY = '2145355c0f23c04710146a3f15230ea1'

TWITTER_API_KEY = '1EZ9FINl6nzPN2ZnRumg'
TWITTER_SECRET = 'xe0p94TWaf5n26bP3KRnI44zKJKzOHqse0RYrQ4V1xA'

BITLY_LOGIN = 'buythebaydev'
BITLY_API_KEY = 'R_bfc558a0b2dd3d5fd9f61a480b749718'
