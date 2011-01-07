from django.conf.urls.defaults import *


urlpatterns = patterns('paypal.views',
    (r'^confirm/$', 'paypal_return'),
    (r'^cancel/$', 'paypal_cancel_return'),
    (r'^ipn/$', 'paypal_ipn'),
)
