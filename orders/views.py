from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from orders.models import Order, ProductInOrder
from products.models import Product


def cart(request):
    """View and edit the user's shopping cart."""
    ProductInOrderFormSet = modelformset_factory(
        ProductInOrder,
        fields=('quantity',),
        max_num=0,
        extra=0,
    )
    order = Order.get_or_create(request)

    if request.method == 'POST':
        # Update the cart quantities
        formset = ProductInOrderFormSet(request.POST, queryset=order.productinorder_set.all())
        if formset.is_valid():
            formset.save()
    else:
        formset = ProductInOrderFormSet(queryset=order.productinorder_set.all())

    # Add the forms into the cart data structure
    cart = order.get_as_cart()
    for i, form in enumerate(formset.forms):
        cart['products'][i]['quantity_form'] = form
    cart['management_form'] = formset.management_form

    return render_to_response('orders/cart.html', {
        'cart': cart,
    }, context_instance=RequestContext(request))

def add(request, product_slug=None):
    """Add a product to the cart."""
    product = get_object_or_404(Product, is_active=True, slug=product_slug)
    order = Order.get_or_create(request)

    # Check if the product is already in the order
    product_in_order = order.productinorder_set.filter(product=product).all()
    if len(product_in_order):
        # Add 1 to the quantity of that product
        product_in_order = product_in_order[0]
        product_in_order.quantity += 1
    else:
        # Add the product to the order
        product_in_order = ProductInOrder(order=order, product=product)
    product_in_order.save()

    # Redirect to the shopping cart
    return HttpResponseRedirect(reverse('orders.views.cart'))

def remove(request, product_slug=None):
    """Remove a product from the cart."""
    product = get_object_or_404(Product, is_active=True, slug=product_slug)
    order = Order.get_or_create(request)

    # Delete the product from the order
    product_in_order = get_object_or_404(ProductInOrder,
        product=product, order=order)
    product_in_order.delete()

    # Redirect to the shopping cart
    return HttpResponseRedirect(reverse('orders.views.cart'))
