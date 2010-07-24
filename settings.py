# Import all the base settings
from env.settings_base import *

# Import the environment-specific settings
from env.local_settings import ENV
env_settings = __import__('env.settings_%s' % ENV, globals(), locals(), [], -1)
for key, value in vars(getattr(env_settings, 'settings_%s' % ENV)).iteritems():
    if not key.startswith('_'):
        globals()[key] = value

# Override with any settings in local_settings
from env.local_settings import *
