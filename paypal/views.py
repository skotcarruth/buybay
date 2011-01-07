from decimal import Decimal
import logging
import urllib
import urllib2
import urlparse

from django.conf import settings
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from mail.models import Message
from paypal.models import IPNRecord
from orders.models import Order


def paypal_return(request):
    """Displays a payment confirmation page."""
    # Retrieve order data from PayPal via PDT
    pdt_data = {}
    transaction_id = request.GET.get('tx')
    paypal_url = settings.PAYPAL_POST_URL
    params = {
        'cmd': '_notify-synch',
        'tx': transaction_id,
        'at': settings.PAYPAL_PDT_TOKEN,
    }
    print 'params', params
    req = urllib2.Request(paypal_url, urllib.urlencode(params))
    req.add_header('Content-type', 'application/x-www-form-urlencoded')
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError:
        logging.warning('Unable to contact PayPal to retrieve PDT data.')
    else:
        pdt_status = response.readline().strip()
        if response.code != 200 or pdt_status != 'SUCCESS':
            logging.warning('Unable to retrieve order data via PDT. Received '
                'response: \n%s\n%s' % (pdt_status, response.read()))
        else:
            # Parse the PDT response
            pdt_data = dict(urlparse.parse_qsl(
                '&'.join(map(lambda s: s.strip(), response))
            ))

    # Get the order referenced by the PDT data
    try:
        order = Order.objects.get(invoice_id=pdt_data.get('invoice'))
    except Order.DoesNotExist:
        order = None

    # Clear the user's shopping cart
    request.session['order_id'] = None

    return render_to_response('paypal/paypal_return.html', {
        'pdt_data': pdt_data,
        'order': order,
    }, context_instance=RequestContext(request))

def paypal_cancel_return(request):
    """Displays a canceled payment page."""
    # Clear the user's shopping cart
    request.session['order_id'] = None

    return render_to_response('paypal/paypal_cancel_return.html', {
    }, context_instance=RequestContext(request))

@csrf_exempt
def paypal_ipn(request):
    """Handles PayPal IPN notifications."""
    if not request.method == 'POST':
        logging.warning('IPN view hit but not POSTed to. Attackers?')
        raise Http404
    paypal_url = settings.PAYPAL_POST_URL

    # Ack and verify the message with paypal
    params = request.POST.copy()
    if params.get('_fake_paypal_verification') == settings.SECRET_KEY:
        pass
    else:
        params['cmd'] = '_notify-validate'
        req = urllib2.Request(paypal_url, urllib.urlencode(params))
        req.add_header('Content-type', 'application/x-www-form-urlencoded')
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            logging.error('Unable to contact PayPal to ack the message.')
            raise Http404 # Let PayPal resend later and try again
        if response.code != 200 or response.readline() != 'VERIFIED':
            logging.warning('IPN view could not verify the message with '
                'PayPal. Original: %r' % request.POST)
            return HttpResponse('Ok (unverified)')
    params = request.POST.copy()

    # Verify that the message is for our business
    business = params.get('business')
    if business and business != settings.PAYPAL_BUSINESS:
        logging.warning('IPN received for a random business. Weird.')
        return HttpResponse('Ok (wrong business)')

    # Save the notification and ensure it's not a duplicate
    transaction_id = params.get('txn_id')
    if not transaction_id:
        logging.warning('No transaction id provided.')
        return HttpResponse('Ok (no id)')
    try:
        record = IPNRecord(transaction_id=transaction_id, data=repr(params))
        record.save()
    except IntegrityError:
        logging.warning('IPN was duplicate. Probably nothing to worry about.')
        return HttpResponse('Ok (duplicate)')

    # Verify that the status is Completed
    if params.get('payment_status') != 'Completed':
        logging.warning('Status not completed. Taking no action.')
        return HttpResponse('Ok (not completed)')

    # Verify that the amount paid matches the cart amount
    invoice_id = params.get('invoice')
    try:
        order = Order.objects.get(invoice_id=invoice_id)
    except Order.DoesNotExist:
        logging.warning('Could not find corresponding Order.')
        return HttpResponse('Ok (no order)')
    order_total = Decimal(str(order.get_as_cart()['total'])).quantize(Decimal('0.01'))
    paypal_total = Decimal(str(params['mc_gross'])).quantize(Decimal('0.01'))
    if order_total != paypal_total:
        logging.warning('PayPal payment amount (%.2f) did not match order '
            'amount (%.2f)!' % (paypal_total, order_total))
        order.status = Order.PROCESSING_ERROR
        order.save()
        return HttpResponse('Ok (wrong amount)')

    # Take action! Save the details of the order
    order.status = Order.PAYMENT_CONFIRMED

    order.user_email = params.get('payer_email')
    order.user_firstname = params.get('first_name')
    order.user_lastname = params.get('last_name')
    order.user_shiptoname = params.get('address_name')
    order.user_shiptostreet = params.get('address_street')
    order.user_shiptocity = params.get('address_city')
    order.user_shiptostate = params.get('address_state')
    order.user_shiptozip = params.get('address_zip')
    order.user_shiptocountry = params.get('address_country')
    order.user_shiptophonenum = params.get('contact_phone')

    order.paypal_transactionid = params.get('txn_id')
    order.paypal_paymenttype = params.get('payment_type')
    order.paypal_ordertime = params.get('payment_date')
    order.paypal_amt = params.get('mc_gross')
    order.paypal_feeamt = params.get('mc_fee')
    order.paypal_paymentstatus = params.get('payment_status')

    order.paypal_details_dump = params.urlencode()
    order.save()

    # Increment the number of products sold
    for product_in_order in order.productinorder_set.all():
        product = product_in_order.product
        product.current_quantity += product_in_order.quantity
        product.save()

    # Create a confirmation email to be sent
    context = {'order': order}
    message = Message()
    message.to_email = order.user_email
    message.from_email = settings.DEFAULT_FROM_EMAIL
    message.subject = render_to_string('mail/order_confirmation_subject.txt', context)
    message.body_text = render_to_string('mail/order_confirmation.txt', context)
    message.body_html = render_to_string('mail/order_confirmation.html', context)
    message.save()

    logging.info('PayPal payment recorded successfully.')
    return HttpResponse('Ok')
