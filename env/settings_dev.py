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

PAYPAL_SERVER = 'https://api-3t.sandbox.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.sandbox.paypal.com/webscr'
PAYPAL_USER = 'merch_1281066320_biz_api1.gmail.com'
PAYPAL_PASS = '1281066328'
PAYPAL_SIGNATURE = 'AP5ErZnuVaoE-u3JZQnMRJXRlcHnA-KyqL7eaN1CbAp5nWvcGzwLwPWT'

FACEBOOK_APP_ID = '132846116761716'
FACEBOOK_API_KEY = '6c600d30e9f6b4d4d6dea40f9ff04819'
FACEBOOK_SECRET_KEY = '2145355c0f23c04710146a3f15230ea1'
