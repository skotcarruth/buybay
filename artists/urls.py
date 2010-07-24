from django.conf.urls.defaults import *


urlpatterns = patterns('artists.views',
    (r'^$', 'index'),
    (r'^(?P<artist_slug>[A-Za-z0-9_-]+)/$', 'artist'),
)
