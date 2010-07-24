from django.db import models


class Product(models.Model):
    """A product in the collection."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_end = models.DateTimeField()

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_ts']

class ProductImage(models.Model):
    """An image for a product."""
    product = models.ForeignKey('Product')
    image = models.ImageField(upload_to='uploads/product_images/')
    order = models.IntegerField(default=0)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_ts']
