from django.conf.urls.defaults import *


urlpatterns = patterns('blog.views',
    (r'^$', 'index'),
    (r'^(?P<year>\d{4})/(?P<month>[A-Za-z]{3})/$', 'archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>[A-Za-z]{3})/(?P<day>\d{1,2})/(?P<slug>[A-Za-z0-9._-]+)/$', 'post'),
    (r'^(?P<tag_slug>[A-Za-z0-9._-]+)/$', 'tag'),
)
