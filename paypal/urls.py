from django.conf.urls.defaults import *


urlpatterns = patterns('paypal.views',
    (r'^ipn/$', 'ipn'),
)
