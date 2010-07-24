from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from products.models import Product


def index(request):
    """An index of the entire product collection."""
    products = Product.objects.filter(is_active=True).all()
    return render_to_response('products/index.html', {
        'products': products,
    }, context_instance=RequestContext(request))

def product(request, product_slug=None):
    """A detail page for a product."""
    product = get_object_or_404(Product, is_active=True, slug=product_slug)
    return render_to_response('products/product.html', {
        'product': product,
    }, context_instance=RequestContext(request))
