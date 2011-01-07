from decimal import Decimal
import logging
import urllib
import urllib2

from django.conf import settings
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from paypal.models import IPNRecord
from orders.models import Order


@csrf_exempt
def ipn(request):
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
    order.user_shiptocountrycode = params.get('address_country_code')
    order.user_shiptophonenum = params.get('contact_phone')

    order.paypal_transactionid = params.get('txn_id')
    order.paypal_paymenttype = params.get('payment_type')
    order.paypal_ordertime = params.get('payment_date')
    order.paypal_amt = params.get('mc_gross')
    order.paypal_feeamt = params.get('mc_fee')
    order.paypal_paymentstatus = params.get('payment_status')

    order.paypal_details_dump = params.urlencode()
    order.save()
    logging.info('PayPal payment recorded successfully.')
    return HttpResponse('Ok')

