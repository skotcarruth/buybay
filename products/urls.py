from django.conf.urls.defaults import *


urlpatterns = patterns('products.views',
    (r'^$', 'index'),
    (r'^(?P<product_slug>[A-Za-z0-9_-]+)/$', 'product'),
)
