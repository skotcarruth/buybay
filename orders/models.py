from decimal import Decimal

from django.db import models


class Order(models.Model):
    """A saved shopping cart."""
    SHOPPING_CART = 0
    ORDER_COMPLETED = 1
    PAYMENT_CONFIRMED = 2
    STATUS_CHOICES = (
        (SHOPPING_CART, 'Shopping Cart'),
        (ORDER_COMPLETED, 'Order Completed'),
        (PAYMENT_CONFIRMED, 'Payment Confirmed'),
    )

    session_id = models.CharField(max_length=40, blank=True, null=True)
    products = models.ManyToManyField('products.Product', through='ProductInOrder', related_name='order_products')
    donation = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=SHOPPING_CART)

    created_ts = models.DateTimeField('Created', auto_now_add=True)

    # Contact and shipping info from the payment
    user_email = models.CharField('email', max_length=200, blank=True)
    user_salutation = models.CharField('salutation', max_length=20, blank=True)
    user_firstname = models.CharField('first name', max_length=25, blank=True)
    user_middlename = models.CharField('last name', max_length=25, blank=True)
    user_lastname = models.CharField('middle name', max_length=25, blank=True)
    user_suffix = models.CharField('suffix', max_length=12, blank=True)
    user_shiptoname = models.CharField('shipping name', max_length=32, blank=True)
    user_shiptostreet = models.CharField('street', max_length=100, blank=True)
    user_shiptostreet2 = models.CharField('street 2', max_length=100, blank=True)
    user_shiptocity = models.CharField('city', max_length=40, blank=True)
    user_shiptostate = models.CharField('state', max_length=40, blank=True)
    user_shiptozip = models.CharField('ZIP', max_length=20, blank=True)
    user_shiptocountrycode = models.CharField('country', max_length=2, blank=True)
    user_shiptophonenum = models.CharField('phone', max_length=20, blank=True)

    # Some of the payment info returned
    paypal_transactionid = models.CharField('transaction ID', max_length=25, blank=True)
    paypal_paymenttype = models.CharField('payment type', max_length=15, blank=True)
    paypal_ordertime = models.DateTimeField('date (UTC)', blank=True, null=True)
    paypal_amt = models.DecimalField('amount', max_digits=10, decimal_places=2, blank=True, null=True)
    paypal_feeamt = models.DecimalField('PayPal fee', max_digits=10, decimal_places=2, blank=True, null=True)
    paypal_settleamt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paypal_taxamt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paypal_paymentstatus = models.CharField('status', max_length=25, blank=True)
    paypal_notetext = models.TextField('note text', blank=True)

    # Dump of the return values of these paypal calls
    paypal_details_dump = models.TextField(blank=True)
    paypal_payment_dump = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_ts']

    def __unicode__(self):
        return 'Order #%d (%s)' % (self.pk, self.get_status_display())

    def get_as_cart(self):
        """Returns all the info for displaying a shopping-cart-style representation."""
        cart = {
            'products': [],
            'subtotal': Decimal('0.00'),
        }
        for product_in_order in self.productinorder_set.all():
            product_in_cart = {
                'product': product_in_order.product,
                'quantity': product_in_order.quantity,
                'total_price': product_in_order.product.price * product_in_order.quantity,
            }
            cart['products'].append(product_in_cart)
            cart['subtotal'] += product_in_cart['total_price']
        cart['tax'] = self.get_tax_amount(cart['subtotal'])
        cart['shipping'] = self.get_shipping_amount(self.get_total_items())
        cart['donation'] = self.donation
        cart['total'] = cart['subtotal'] + cart['tax'] + cart['shipping'] + cart['donation']
        return cart

    def get_tax_amount(self, subtotal):
        """Returns the amount of tax for the items in the cart."""
        # TODO: make this for rillz
        TAX_RATE = Decimal('0.0925')
        return subtotal * TAX_RATE

    def get_shipping_amount(self, total_items):
        """Returns the amount of shipping charges for the items in the cart."""
        # TODO: make this for rillz too
        SHIPPING_PER_ITEM = Decimal('0.00')
        return total_items * SHIPPING_PER_ITEM

    def get_total_items(self):
        """Returns the number of products in the order."""
        return sum([p.quantity for p in self.productinorder_set.all()])
    get_total_items.short_description = 'Items'

    def get_subtotal(self):
        """Returns the total price of all the products in the order."""
        return sum([p.quantity * p.product.price for p in self.productinorder_set.all()])

    def get_total_price_display(self):
        return '$%.2f' % self.get_total_price()
    get_total_price_display.short_description = 'Total'

    @classmethod
    def get_or_create(cls, request, save=True):
        """Return the order attached to this request session, if exists, or create one."""
        order = None
        order_id = request.session.get('order_id', None)
        if order_id:
            try:
                order = cls.objects.get(id=order_id)
            except cls.DoesNotExist:
                pass
        if not order:
            order = cls(session_id=request.session.session_key)
            if save:
                order.save()
            request.session['order_id'] = order.id
        return order

class ProductInOrder(models.Model):
    """An M2M table for storing extra info on a product in a cart."""
    order = models.ForeignKey('Order')
    product = models.ForeignKey('products.Product')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['product']
        verbose_name_plural = 'Products In This Order'
        unique_together = ('order', 'product',)

    def __unicode__(self):
        return '%s in %s' % (unicode(self.product), unicode(self.order))
