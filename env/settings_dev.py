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
