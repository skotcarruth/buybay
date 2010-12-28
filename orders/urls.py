from django.conf.urls.defaults import *


urlpatterns = patterns('orders.views',
    (r'^$', 'cart'),
    (r'^update/$', 'update_cart'),
    (r'^add/(?P<product_slug>[A-Za-z0-9_-]+)/$', 'add'),
    (r'^remove/(?P<product_slug>[A-Za-z0-9_-]+)/$', 'remove'),
    (r'^standard_confirmation/$', 'standard_confirmation'),
    (r'^standard_notify/$', 'standard_notify'),
)
