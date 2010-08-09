from django.conf.urls.defaults import *


urlpatterns = patterns('products.views',
    (r'^$', 'index'),
    (r'^tag/(?P<tag_slug>[A-Za-z0-9_-]+)/$', 'tag'),
    (r'^(?P<product_slug>[A-Za-z0-9_-]+)/$', 'product'),
)
