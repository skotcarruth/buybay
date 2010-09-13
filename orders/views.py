from datetime import datetime
from decimal import Decimal
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from orders.forms import DonationForm
from orders.models import Order, ProductInOrder
from orders.paypal import paypal, PayPalUnavailable, PayPalErrorResponse
from mail.models import Message
from products.models import Product
from buybay.views import json_response


def cart(request):
    """View and edit the user's shopping cart."""
    order = Order.get_or_create(request)
    donation_form = DonationForm(instance=order)

    if request.method == 'POST':
        donation_form = DonationForm(request.REQUEST, instance=order)
        if donation_form.is_valid():
            donation_form.save()
            return HttpResponseRedirect(reverse('orders.views.purchase'))

    cart = order.get_as_cart()

    return render_to_response('orders/cart.html', {
        'cart': cart,
        'donation_form': donation_form,
    }, context_instance=RequestContext(request))

@json_response
def update_cart(request):
    """Updates the user's shopping cart."""
    order = Order.get_or_create(request)
    donation_form = DonationForm(request.REQUEST, instance=order)
    if donation_form.is_valid():
        donation_form.save()
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
        if settings.DEBUG:
            raise
        else:
            messages.error(request, 'Sorry, there was an error with PayPal. Please contact us for more info.')

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
    print order.get_as_cart()
    try:
        payment = paypal.do_express_checkout_payment(token, payer_id, order.get_as_cart())
    except PayPalErrorResponse:
        if settings.DEBUG:
            raise
        else:
            messages.error(request, 'Sorry, there was an error with PayPal. Please contact us for more info.')
            return HttpResponseRedirect(reverse('orders.views.cart'))

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

    # Mark the order as paid
    order.status = Order.PAYMENT_CONFIRMED
    order.save()

    # Create a confirmation email to be sent
    context = {'order': order}
    message = Message()
    message.to_email = order.user_email
    message.from_email = settings.DEFAULT_FROM_EMAIL
    message.subject = render_to_string('mail/order_confirmation_subject.txt', context)
    message.body_text = render_to_string('mail/order_confirmation.txt', context)
    message.body_html = render_to_string('mail/order_confirmation.html', context)
    message.save()

    # Clear the user's shopping cart
    request.session['order_id'] = None

    return render_to_response('orders/confirmation.html', {
        'order': order,
    }, context_instance=RequestContext(request))
