from django.conf import settings
from django.test import TestCase

from orders.models import Order, ProductInOrder
from paypal.models import IPNRecord
from products.models import Product


class TestPayPalIPN(TestCase):
    def setUp(self):
        self.ipn_record = IPNRecord(
            transaction_id=1,
            data='a=1',
        )
        self.ipn_record.save()
        self.order = Order(
            donation=100,
            status=Order.SHOPPING_CART,
        )
        self.order.save()
        self.product = Product(
            name='Test Product',
            slug='test-product',
            price=500,
            tax_deductible=50,
            min_quantity=0,
            max_quantity=10,
            current_quantity=5,
            status=Product.FOR_SALE,
        )
        self.product.save()
        self.product_in_order = ProductInOrder(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        self.product_in_order.save()

    def test_ipn_error_conditions(self):
        # Anything besides POST gets a 404
        response = self.client.get('/paypal/ipn/')
        self.assertEqual(response.status_code, 404)

        # Can't verify message with PayPal
        response = self.client.post('/paypal/ipn/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (unverified)')

        # Message not for our business
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': 'whoever@something.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (wrong business)')

        # No transaction ID provided
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': settings.PAYPAL_BUSINESS,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (no id)')

        # Duplicate IPN message received
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': settings.PAYPAL_BUSINESS,
            'txn_id': '1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (duplicate)')

        # Status is not Completed
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': settings.PAYPAL_BUSINESS,
            'txn_id': '2',
            'payment_status': 'Waiting',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (not completed)')

        # No matching order
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': settings.PAYPAL_BUSINESS,
            'txn_id': '3',
            'payment_status': 'Completed',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (no order)')

        # Payment for wrong amount
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': settings.PAYPAL_BUSINESS,
            'txn_id': '4',
            'payment_status': 'Completed',
            'invoice': self.order.invoice_id,
            'mc_gross': '1.00',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok (wrong amount)')

    def test_ipn_success_conditions(self):
        # Order marked as paid
        response = self.client.post('/paypal/ipn/', {
            '_fake_paypal_verification': settings.SECRET_KEY,
            'business': settings.PAYPAL_BUSINESS,
            'txn_id': '5',
            'payment_status': 'Completed',
            'invoice': self.order.invoice_id,
            'mc_gross': '646.25',
        })
        order = Order.objects.get(pk=self.order.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Ok')
        self.assertEqual(order.status, Order.PAYMENT_CONFIRMED)
        record = IPNRecord.objects.get(transaction_id='5')
        self.assertTrue(record.data)
