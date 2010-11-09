"""Utility classes for interacting with PayPal."""
import urllib
import urllib2
import urlparse

from django.conf import settings
from django.contrib.sites.models import Site


# PayPal ack values (from https://cms.paypal.com/us/cgi-bin/?&cmd=_render-content&content_ID=developer/e_howto_api_nvp_NVPAPIOverview#id09C2F0M01TS__id0869704E04E)
PAYPAL_SUCCESS_VALUES = ('Success', 'SuccessWithWarning',)
PAYPAL_ERROR_VALUES = ('Failure', 'FailureWithWarning', 'Warning',)

class PayPalError(Exception):
    pass

class PayPalUnavailable(PayPalError):
    pass

class PayPalErrorResponse(PayPalError):
    pass

class PayPalService(object):
    base_params = {
        'USER': settings.PAYPAL_USER,
        'PWD': settings.PAYPAL_PASS,
        'SIGNATURE': settings.PAYPAL_SIGNATURE,
        'VERSION': settings.PAYPAL_VERSION,
    }

    def _query_url(self, url):
        try:
            response = urllib2.urlopen(url, timeout=10)
        except urllib2.URLError:
            raise PayPalUnavailable('Could not reach PayPal service')
        response = dict(urlparse.parse_qsl(response.read()))
        if response['ACK'] in PAYPAL_ERROR_VALUES:
            raise PayPalErrorResponse('PayPal returned an error (%s: %s)' %
                (response.get('L_SHORTMESSAGE0', ''), response.get('L_LONGMESSAGE0', '')))
        return response

    def set_express_checkout(self, cart, return_url, cancel_url):
        """
        Takes an amount and success and failure URLs. Queries PayPal for an 
        express checkout session and token. Returns the URL to redirect the 
        user to.
        """
        # Query PayPal for the express checkout session token
        params = {
            'METHOD': 'SetExpressCheckout',
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'PAYMENTREQUEST_0_AMT': '%.2f' % cart['total'],
            'PAYMENTREQUEST_0_CURRENCYCODE': 'USD',
            'PAYMENTREQUEST_0_ITEMAMT': '%.2f' % (cart['subtotal'] + cart['donation']),
            'PAYMENTREQUEST_0_SHIPPINGAMT': '%.2f' % cart['shipping'],
            'PAYMENTREQUEST_0_TAXAMT': '%.2f' % cart['tax'],
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
            'PAYMENTREQUEST_0_NOTETEXT': 1,
        }
        params.update(self.base_params)
        # Add the cart items to the params
        for i, product_in_cart in enumerate(cart['products']):
            params.update({
                'L_PAYMENTREQUEST_0_NAME%d' % i: product_in_cart['product'].name,
                'L_PAYMENTREQUEST_0_AMT%d' % i: '%.2f' % product_in_cart['product'].price,
                'L_PAYMENTREQUEST_0_QTY%d' % i: product_in_cart['quantity'],
                'L_PAYMENTREQUEST_0_ITEMURL%d' % i: 'http://%s%s' % (
                    Site.objects.get_current().domain,
                    product_in_cart['product'].get_absolute_url()),
            })
        # Add the optional donation to the params
        if cart['donation']:
            i = len(cart['products'])
            params.update({
                'L_PAYMENTREQUEST_0_NAME%d' % i: 'Donation',
                'L_PAYMENTREQUEST_0_AMT%d' % i: '%.2f' % cart['donation'],
                'L_PAYMENTREQUEST_0_QTY%d' % i: 1,
            })
        # Hit the PayPal API
        url = '%s?%s' % (settings.PAYPAL_SERVER, urllib.urlencode(params))
        response = self._query_url(url)
        token = response['TOKEN']

        # Form the URL to send the user to the checkout on PayPal
        params = {
            'cmd': '_express-checkout',
            'token': token,
            'useraction': 'commit',
        }
        checkout_url = '%s?%s' % (settings.PAYPAL_CHECKOUT_URL, urllib.urlencode(params))
        return checkout_url

    def get_express_checkout_details(self, token):
        """
        Pass in the token returned from the PayPal payment page. Returns a 
        dict of the details provided by PayPal about this transaction and user.
        """
        params = {
            'METHOD': 'GetExpressCheckoutDetails',
            'TOKEN': token,
        }
        params.update(self.base_params)
        url = '%s?%s' % (settings.PAYPAL_SERVER, urllib.urlencode(params))
        response = self._query_url(url)
        return response

    def do_express_checkout_payment(self, token, payer_id, cart):
        """
        Completes the express checkout payment. 
        """
        params = {
            'METHOD': 'DoExpressCheckoutPayment',
            'TOKEN': token,
            'PAYERID': payer_id,
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
            'PAYMENTREQUEST_0_AMT': '%.2f' % cart['total'],
            'PAYMENTREQUEST_0_CURRENCYCODE': 'USD',
        }
        params.update(self.base_params)
        url = '%s?%s' % (settings.PAYPAL_SERVER, urllib.urlencode(params))
        response = self._query_url(url)
        return response

paypal = PayPalService()
