from django.conf.urls.defaults import *


urlpatterns = patterns('flatcontent.views',
    (r'^(?P<page_slug>[A-Za-z0-9._-]+)/$', 'page'),
)
