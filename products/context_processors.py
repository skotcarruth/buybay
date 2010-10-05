from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404

from products.models import Tag


def tags(request):
    """Adds a list of product tags to the context."""
    # Don't waste the DB hits if it's not a products page
    try:
        view, args, kwargs = resolve(request.path)
    except Resolver404:
        return {}
    if view.__module__ != 'products.views':
        return {}

    # Return the list of active tags
    return {'product_tags': Tag.objects.active()}

def settings_context(request):
    """Adds the settings object to the context."""
    return {'settings': settings}
