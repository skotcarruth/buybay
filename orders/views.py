from datetime import datetime, date, time
from decimal import Decimal
from functools import wraps
import json

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from orders.forms import OrderForm
from orders.models import Order, ProductInOrder
from products.models import Product


def _json_prep(data):
    """Recursively converts values to JSON-serializable alternatives."""
    if isinstance(data, (list, tuple, set, frozenset)):
        return [_json_prep(item) for item in data]
    if isinstance(data, dict):
        return dict([(str(key), _json_prep(value)) for key, value in data.iteritems()])
    if isinstance(data, basestring):
        return str(data)
    if isinstance(data, Decimal):
        return float(data)
    if isinstance(data, (date, time, datetime)):
        return str(data)
    if isinstance(data, models.Model):
        return None
    return data

def json_response(view):
    """
    The view function should return a normal Python object (JSON-serializable,
    please). The wrapper will then convert this to JSON and return an
    appropriate HttpResponse object.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        data = view(request, *args, **kwargs)
        return HttpResponse(json.dumps(_json_prep(data)), mimetype='application/javascript')
    return wrapper

def cart(request):
    """View and edit the user's shopping cart."""
    order = Order.get_or_create(request)
    order_form = OrderForm(prefix='btb', instance=order)

    # if request.method == 'POST':
    #     order_form = OrderForm(request.REQUEST, prefix='btb', instance=order)
    #     if order_form.is_valid():
    #         order_form.save()
    #         return HttpResponseRedirect(reverse('orders.views.purchase'))

    cart = order.get_as_cart()

    return render_to_response('orders/cart.html', {
        'cart': cart,
        'order_form': order_form,
        'paypal_post_url': settings.PAYPAL_POST_URL,
        'paypal_business': settings.PAYPAL_BUSINESS,
        'paypal_currency_code': settings.PAYPAL_CURRENCY_CODE,
        'paypal_invoice_id': order.invoice_id,
        'paypal_return_url': reverse('paypal.views.paypal_return'),
        'paypal_cancel_return_url': reverse('paypal.views.paypal_cancel_return'),
    }, context_instance=RequestContext(request))

@json_response
def update_cart(request):
    """Updates the user's shopping cart."""
    order = Order.get_or_create(request)
    order_form = OrderForm(request.REQUEST, prefix='btb', instance=order)
    if order_form.is_valid():
        order = order_form.save()
        return order.get_as_cart()
    return False

def add(request, product_slug=None):
    """Add a product to the cart."""
    product = get_object_or_404(Product.objects.active(), slug=product_slug)
    order = Order.get_or_create(request)
    if product.can_be_purchased():
        # Check if the product is already in the order
        product_in_order = order.productinorder_set.filter(product=product).all()
        if len(product_in_order):
            # Disallow adding more than one of any product
            messages.warning(request, 'You can only add one of each product to your cart.')
            # # Add 1 to the quantity of that product
            # product_in_order = product_in_order[0]
            # product_in_order.quantity += 1
            # messages.success(request, 'Added another "%s" to your cart.' % product.name)
        else:
            # Add the product to the order
            product_in_order = ProductInOrder(order=order, product=product)
            messages.success(request, 'Added "%s" to your cart.' % product.name)
            product_in_order.save()
    else:
        messages.error(request, 'This product is not currently available for purchase.')

    # Redirect to the shopping cart
    return HttpResponseRedirect(reverse('orders.views.cart'))

def remove(request, product_slug=None):
    """Remove a product from the cart."""
    product = get_object_or_404(Product.objects.active(), slug=product_slug)
    order = Order.get_or_create(request)

    # Delete the product from the order
    product_in_order = get_object_or_404(ProductInOrder,
        product=product, order=order)
    product_in_order.delete()
    messages.success(request, 'Removed "%s" from your cart.' % product.name)

    # Redirect to the shopping cart
    return HttpResponseRedirect(reverse('orders.views.cart'))
