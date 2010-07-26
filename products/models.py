from django.db import models


class Product(models.Model):
    """A product in the collection."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_end = models.DateTimeField()
    artists = models.ManyToManyField('artists.Artist')

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_ts']

    def __unicode__(self):
        return u'%s ($%.2f)' % (self.name, self.price)

    @models.permalink
    def get_absolute_url(self):
        return ('products.views.product', (), {'product_slug': self.slug})

    def active_artists(self):
        return self.artists.filter(is_active=True)

class ProductImage(models.Model):
    """An image for a product."""
    product = models.ForeignKey('Product')
    image = models.ImageField(upload_to='uploads/product_images/')
    order = models.IntegerField(default=0)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_ts']

    def __unicode__(self):
        return u'Image %d: %s' % (self.order, self.product.name)
