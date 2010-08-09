from django.core.urlresolvers import resolve
from products.models import Tag


def tags(request):
    """Adds a list of product tags to the context."""
    # Don't waste the DB hits if it's not a products page
    view, args, kwargs = resolve(request.path)
    if view.__module__ != 'products.views':
        return {}

    # Return the list of active tags
    return {'product_tags': Tag.objects.active()}
