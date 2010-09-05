from datetime import datetime
from decimal import Decimal
import json

from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from orders.models import Order, ProductInOrder
from orders.paypal import paypal, PayPalUnavailable, PayPalErrorResponse
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
            messages.success(request, 'Updated your shopping cart quantities.')
        else:
            messages.error(request, 'Could not update your cart quantities. Please try again.')
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
    product = get_object_or_404(Product.objects.active(), slug=product_slug)
    order = Order.get_or_create(request)

    # Check if the product is already in the order
    product_in_order = order.productinorder_set.filter(product=product).all()
    if len(product_in_order):
        # Add 1 to the quantity of that product
        product_in_order = product_in_order[0]
        product_in_order.quantity += 1
        messages.success(request, 'Added another "%s" to your cart.' % product.name)
    else:
        # Add the product to the order
        product_in_order = ProductInOrder(order=order, product=product)
        messages.success(request, 'Added "%s" to your cart.' % product.name)
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
    messages.success(request, 'Removed "%s" from your cart.' % product.name)

    # Redirect to the shopping cart
    return HttpResponseRedirect(reverse('orders.views.cart'))

def purchase(request):
    """Sets up a PayPal express checkout transaction to purchase their cart."""
    order = Order.get_or_create(request)
    cart = order.get_as_cart()
    if cart['total'] <= 0:
        messages.error(request, 'You have to add something to your cart before you check out.')
        return HttpResponseRedirect(reverse('orders.views.cart'))

    # Handle the PayPal interaction
    domain = Site.objects.get_current().domain
    return_url = 'http://%s%s' % (domain, reverse('orders.views.confirmation'))
    cancel_url = 'http://%s%s' % (domain, reverse('orders.views.cart'))
    next_url = cancel_url
    try:
        next_url = paypal.set_express_checkout(cart, return_url, cancel_url)
    except PayPalUnavailable:
        messages.error(request, 'Sorry, we were unable to reach PayPal at the moment. Please try again later.')
    except PayPalErrorResponse as e:
        messages.error(request, 'Sorry, there was an error with PayPal. Please contact us for more info.')
        print e

    # Redirect to the Paypal checkout (or back to the cart if errors)
    return HttpResponseRedirect(next_url)

def confirmation(request):
    """Confirms a successful payment for the order."""
    order = Order.get_or_create(request)
    token = request.GET.get('token', None)
    payer_id = request.GET.get('PayerID', None)
    if not token or not payer_id:
        messages.error(request, 'Sorry, we were unable to process your PayPal payment. Please try again later.')
        return HttpResponseRedirect(reverse('orders.views.cart'))

    # Get the transaction details from PayPal
    details = paypal.get_express_checkout_details(token)

    # Confirm the transaction with PayPal, and update the order
    payment = paypal.do_express_checkout_payment(token, payer_id, order.get_as_cart())

    # Finalize the order with payment details
    order.user_email = details.get('EMAIL', '')
    order.user_salutation = details.get('SALUTATION', '')
    order.user_firstname = details.get('FIRSTNAME', '')
    order.user_middlename = details.get('MIDDLENAME', '')
    order.user_lastname = details.get('LASTNAME', '')
    order.user_suffix = details.get('SUFFIX', '')
    order.user_shiptoname = details.get('PAYMENTREQUEST_0_SHIPTONAME', '')
    order.user_shiptostreet = details.get('PAYMENTREQUEST_0_SHIPTOSTREET', '')
    order.user_shiptostreet2 = details.get('PAYMENTREQUEST_0_SHIPTOSTREET2', '')
    order.user_shiptocity = details.get('PAYMENTREQUEST_0_SHIPTOCITY', '')
    order.user_shiptostate = details.get('PAYMENTREQUEST_0_SHIPTOSTATE', '')
    order.user_shiptozip = details.get('PAYMENTREQUEST_0_SHIPTOZIP', '')
    order.user_shiptocountrycode = details.get('PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE', '')
    order.user_shiptophonenum = details.get('PAYMENTREQUEST_0_SHIPTOPHONENUM', '')

    # Some of the payment info returned
    order.paypal_transactionid = payment.get('PAYMENTINFO_0_TRANSACTIONID', '')
    order.paypal_paymenttype = payment.get('PAYMENTINFO_0_PAYMENTTYPE', '')
    order.paypal_ordertime = datetime.strptime(payment['PAYMENTINFO_0_ORDERTIME'], '%Y-%m-%dT%H:%M:%SZ') if 'PAYMENTINFO_0_ORDERTIME' in payment else None
    order.paypal_amt = Decimal(payment.get('PAYMENTINFO_0_AMT', '0.00'))
    order.paypal_feeamt = Decimal(payment.get('PAYMENTINFO_0_FEEAMT', '0.00'))
    order.paypal_settleamt = Decimal(payment.get('PAYMENTINFO_0_SETTLEAMT', '0.00'))
    order.paypal_taxamt = Decimal(payment.get('PAYMENTINFO_0_TAXAMT', '0.00'))
    order.paypal_paymentstatus = payment.get('PAYMENTINFO_0_PAYMENTSTATUS', '')

    # Dump of the return values of these paypal calls
    order.paypal_details_dump = json.dumps(details)
    order.paypal_payment_dump = json.dumps(payment)

    order.save()

    # Clear the user's shopping cart
    request.session['order_id'] = None

    return render_to_response('orders/confirmation.html', {
        'order': order,
    }, context_instance=RequestContext(request))
