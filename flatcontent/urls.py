from django.conf.urls.defaults import *


urlpatterns = patterns('flatcontent.views',
    (r'^$', 'index'),
    (r'^(?P<page_slug>[A-Za-z0-9._-]+)/$', 'page'),
)
