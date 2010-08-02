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

    session = models.ForeignKey('sessions.Session')
    products = models.ManyToManyField('products.Product', through='ProductInOrder')
    status = models.IntegerField(choices=STATUS_CHOICES, default=SHOPPING_CART)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_ts']

    def __unicode__(self):
        return 'Order #%d (%s)' % (self.pk, self.get_status_display())

    def get_as_cart(self):
        """Returns all the info for displaying a shopping-cart-style representation."""
        cart = {
            'products': [],
            'total_price': Decimal('0.00'),
        }
        for product_in_order in self.productinorder_set.all():
            product_in_cart = {
                'product': product_in_order.product,
                'quantity': product_in_order.quantity,
                'total_price': product_in_order.product.price * product_in_order.quantity,
            }
            cart['products'].append(product_in_cart)
            cart['total_price'] += product_in_cart['total_price']
        return cart

    def get_total_items(self):
        """Returns the number of products in the order."""
        return sum([p.quantity for p in self.productinorder_set.all()])

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
        verbose_name_plural = 'products in orders'
        unique_together = ('order', 'product',)

    def __unicode__(self):
        return '%s in %s' % (unicode(self.product), unicode(self.order))
