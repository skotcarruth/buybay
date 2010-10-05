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

FACEBOOK_APP_ID = '158099770871210'
FACEBOOK_API_KEY = 'ccf967dafd80ed309f2e2def37b6fb3a'
FACEBOOK_SECRET_KEY = '1597a151223a4de9921eeadb597a496c'

TWITTER_API_KEY = 't6Z0Vmm2G0wP37dqcTiHvw'
TWITTER_SECRET = 'EUrgJBSNlBY96ccU8DC8AYewXPpLsjIY0Bl3ZHgji4'

BITLY_LOGIN = 'buythebaystaging'
BITLY_API_KEY = 'R_33f78177f8e42146e7f582bd65de3302'
