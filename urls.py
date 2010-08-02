import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

sitemaps = {}

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    (r'^collection/', include('products.urls')),
    (r'^artists/', include('artists.urls')),
    (r'^news/', include('blog.urls')),
    (r'^cart/', include('orders.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Flat pages exist right off the root url, so this goes last as a catchall
    (r'^', include('flatcontent.urls')),
)

if settings.ENV == 'dev':
    # Files that should be served by Apache in prod
    STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    urlpatterns += patterns('',
        (r'^favicon\.ico$', 'django.views.static.serve', {'document_root': STATIC, 'path': 'images/favicon.ico'}),
        (r'^robots\.txt$', 'django.views.static.serve', {'document_root': STATIC, 'path': 'robots.txt'}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC}),
    )