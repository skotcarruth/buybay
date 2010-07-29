from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GalleryMedia(models.Model):
    """An image for a product."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    image = models.ImageField(upload_to='uploads/gallery_images/', blank=True)
    video = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_ts']
        verbose_name_plural = u'gallery media'

    def __unicode__(self):
        return u'Image %d: %s' % (self.order, self.product.name)

    @property
    def media_type(self):
        if self.image:
            return 'image'
        elif self.video:
            return 'video'
        return None

    def get_media(self):
        return self.image or self.video
