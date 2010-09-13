from django.contrib.contenttypes import generic
from django.db import models

from galleries.models import GalleryMedia


class TagManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Tag(models.Model):
    """A category for products."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = TagManager()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('products.views.tag', (), {'tag_slug': self.slug})

    def num_products(self):
        return self.product_set.count()
    num_products.short_description = 'Products'

SORT_OPTIONS = {
    'name': {'attr': 'name', 'up': '', 'down': '-'},
    'price': {'attr': 'price', 'up': '', 'down': '-'},
    'date': {'attr': 'created_ts', 'up': '-', 'down': ''},
}
STATUS_OPTIONS = {
    'all': None,
    'for_sale': 'FOR_SALE',
    'coming_soon': 'COMING_SOON',
    'archived': 'ARCHIVED',
}
def product_filter(qs, status):
    status = STATUS_OPTIONS.get(status, STATUS_OPTIONS['all'])
    if status is not None:
        return qs.filter(status=getattr(Product, status))
    return qs

def product_sort(qs, sort, sort_dir):
    if sort not in SORT_OPTIONS:
        sort = 'name'
    if sort_dir not in ('up', 'down'):
        sort_dir = 'up'
    ordering = '%s%s' % (SORT_OPTIONS[sort][sort_dir], SORT_OPTIONS[sort]['attr'])
    return qs.order_by(ordering)

class ProductManager(models.Manager):
    def active(self):
        return self.filter(status__in=(Product.COMING_SOON, Product.FOR_SALE, Product.ARCHIVED))

class Product(models.Model):
    """A product in the collection."""
    HIDDEN = 0
    COMING_SOON = 1
    FOR_SALE = 2
    ARCHIVED = 3
    STATUS_CHOICES = (
        (HIDDEN, 'Hidden'),
        (COMING_SOON, 'Coming Soon'),
        (FOR_SALE, 'For Sale'),
        (ARCHIVED, 'Archived'),
    )

    # Basic product info
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    design = models.TextField(blank=True)
    related_info_1 = models.CharField(max_length=400, blank=True)
    related_info_2 = models.CharField(max_length=400, blank=True)
    related_info_3 = models.CharField(max_length=400, blank=True)
    artists = models.ManyToManyField('artists.Artist')
    tags = models.ManyToManyField('Tag', blank=True)

    # Deal and pricing info
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    current_quantity = models.PositiveIntegerField(default=0)

    # Images and video
    name_image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    main_image_1 = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    main_image_2 = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    gallery_media = generic.GenericRelation(GalleryMedia)

    # Metadata and settings
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        ordering = ['-created_ts']

    def __unicode__(self):
        return u'%s ($%.2f, %s)' % (self.name, self.price, self.get_status_display())

    @models.permalink
    def get_absolute_url(self):
        return ('products.views.product', (), {'product_slug': self.slug})

    def can_be_purchased(self):
        """Returns whether the product is currently available for purchase."""
        for_sale = self.status == self.FOR_SALE
        available = self.current_quantity < self.max_quantity
        return for_sale and available

    def active_artists(self):
        return self.artists.filter(is_active=True)

    def get_previous(self):
        """Returns the previous active Product, by created date, or None."""
        previous = Product.objects.active().filter(created_ts__lt=self.created_ts).order_by('-created_ts')
        if previous.exists():
            return previous[0]
        return None

    def get_next(self):
        """Returns the next active Product, by created date, or None."""
        next = Product.objects.active().filter(created_ts__gt=self.created_ts).order_by('created_ts')
        if next.exists():
            return next[0]
        return None

class ProductCommentManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class ProductComment(models.Model):
    """A comment on a product."""
    product = models.ForeignKey('Product')
    facebook_id = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=400)
    thumb_url = models.URLField(verify_exists=False, blank=True)
    comment = models.TextField()

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = ProductCommentManager()

    class Meta:
        ordering = ['created_ts']
        verbose_name = u'comment'

    def __unicode__(self):
        return '%s comment (%s)' % (self.product.name, self.created_ts)
