from django.db import models


class Feature(models.Model):
    """A homepage featured product."""
    product = models.ForeignKey('products.Product', blank=True, null=True)
    image_before = models.ImageField(upload_to='uploads/feature_images/')
    image_after = models.ImageField(upload_to='uploads/feature_images/')
    link_override = models.URLField(verify_exists=False, blank=True,
        help_text=u'By default, the feature links to its product; use this '
        'if you want to pick a different destination.')
    order = models.IntegerField(default=0)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_ts']

    def __unicode__(self):
        return u'Feature: %s' % (self.product.name if self.product else u'[no product]')

    def get_destination_url(self):
        if self.link_override:
            return self.link_override
        if self.product:
            return self.product.get_absolute_url()
        return ''
