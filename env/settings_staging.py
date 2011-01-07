# Settings overrides for the staging environment
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'philosophie_btb',
        'USER': 'philosophie_btb',
        'PASSWORD': '9cc00c8a',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'nweave_buybay'
EMAIL_HOST_PASSWORD = '0e341dd7'
DEFAULT_FROM_EMAIL = 'noreply@buythebay.jeffschenck.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Paypal Express Checkout (lame)
PAYPAL_SERVER = 'https://api-3t.paypal.com/nvp'
PAYPAL_CHECKOUT_URL = 'https://www.paypal.com/cgi-bin/webscr.'
PAYPAL_USER = 'nburdick_api1.healthebay.org'
PAYPAL_PASS = 'BPFL5JQREGCNZ4KL'
PAYPAL_SIGNATURE = 'AkrturaUrjwo1xbii9WwCzlYDWEDA2iWs3FpjP-5TZ0vH3VWMB6nlgwM'

# Paypal Web Standard Payments (less lame)
PAYPAL_CURRENCY_CODE = 'USD'
# PAYPAL_POST_URL = 'https://www.paypal.com/cgi-bin/webscr'
PAYPAL_POST_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
# PAYPAL_BUSINESS = 'nburdick@healthebay.org'
PAYPAL_BUSINESS = 'seller_1294382044_biz@gmail.com'
PAYPAL_PDT_TOKEN = 'eVx9db-kIpQ0w_HsIt335P9Cmf5439r0wZfDt3F8PrtKtmXrjiUhKzMl0N4'

FACEBOOK_APP_ID = '158099770871210'
FACEBOOK_API_KEY = 'ccf967dafd80ed309f2e2def37b6fb3a'
FACEBOOK_SECRET_KEY = '1597a151223a4de9921eeadb597a496c'

TWITTER_API_KEY = 't6Z0Vmm2G0wP37dqcTiHvw'
TWITTER_SECRET = 'EUrgJBSNlBY96ccU8DC8AYewXPpLsjIY0Bl3ZHgji4'

BITLY_LOGIN = 'buythebaystaging'
BITLY_API_KEY = 'R_33f78177f8e42146e7f582bd65de3302'
