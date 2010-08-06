"""Utility classes for interacting with PayPal."""
import urllib
import urllib2
import urlparse

from django.conf import settings


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

    def set_express_checkout(self, amount, return_url, cancel_url):
        """
        Takes an amount and success and failure URLs. Queries PayPal for an 
        express checkout session and token. Returns the URL to redirect the 
        user to.
        """
        # Query PayPal for the express checkout session token
        amount = '%.2f' % amount
        params = {
            'METHOD': 'SetExpressCheckout',
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'PAYMENTREQUEST_0_AMT': amount,
        }
        params.update(self.base_params)
        url = '%s?%s' % (settings.PAYPAL_SERVER, urllib.urlencode(params))
        response = self._query_url(url)
        token = response['TOKEN']

        # Form the URL to send the user to the checkout on PayPal
        params = {
            'cmd': '_express-checkout',
            'token': token,
            'AMT': amount,
            'CURRENCYCODE': 'USD',
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
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

    def do_express_checkout_payment(self, token, payer_id, amount):
        """
        Completes the express checkout payment. 
        """
        amount = '%.2f' % amount
        params = {
            'METHOD': 'DoExpressCheckoutPayment',
            'TOKEN': token,
            'PAYERID': payer_id,
            'PAYMENTACTION': 'Sale',
            'AMT': amount,
            'CURRENCYCODE': 'USD',
        }
        params.update(self.base_params)
        url = '%s?%s' % (settings.PAYPAL_SERVER, urllib.urlencode(params))
        response = self._query_url(url)
        return response

paypal = PayPalService()
