from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from products.models import Product, Tag, product_filter, product_sort


def index(request):
    """An index of the entire product collection."""
    sort = request.GET.get('sort', None)
    sort_dir = request.GET.get('sort_dir', None)
    status = request.GET.get('filter', None)

    # Query for the products, tags
    products = Product.objects.active()
    products = product_filter(products, status)
    products = product_sort(products, sort, sort_dir)
    tags = Tag.objects.active()

    return render_to_response('products/index.html', {
        'products': products,
        'tags': tags,
    }, context_instance=RequestContext(request))

def tag(request, tag_slug=None):
    """A collections page filtered by tag."""
    sort = request.GET.get('sort', None)
    sort_dir = request.GET.get('sort_dir', None)
    status = request.GET.get('filter', None)

    # Query for the products, tags
    tag = get_object_or_404(Tag.objects.active(), slug=tag_slug)
    products = tag.product_set.active()
    products = product_filter(products, status)
    products = product_sort(products, sort, sort_dir)

    return render_to_response('products/tag.html', {
        'tag': tag,
        'products': products,
    }, context_instance=RequestContext(request))

def product(request, product_slug=None):
    """A detail page for a product."""
    product = get_object_or_404(Product.objects.active(), slug=product_slug)
    return render_to_response('products/product.html', {
        'product': product,
        'ratio': float(product.current_quantity) / float(product.max_quantity),
    }, context_instance=RequestContext(request))
