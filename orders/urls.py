from django.conf.urls.defaults import *


urlpatterns = patterns('orders.views',
    (r'^$', 'cart'),
    (r'^add/(?P<product_slug>[A-Za-z0-9_-]+)/$', 'add'),
    (r'^remove/(?P<product_slug>[A-Za-z0-9_-]+)/$', 'remove'),
)
