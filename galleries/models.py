from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


class GalleryMediaManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

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

    objects = GalleryMediaManager()

    class Meta:
        ordering = ['order', '-created_ts']
        verbose_name_plural = u'gallery media'

    def __unicode__(self):
        return u'Media %d: %s' % (self.order, self.content_object.__unicode__())

    def clean(self):
        # Verify that the model has either an image or video
        if not self.image and not self.video:
            raise ValidationError('Either an image or video is requried.')

    @property
    def media_type(self):
        if self.image:
            return 'image'
        elif self.video:
            return 'video'
        return None

    def get_media(self):
        return self.image or self.video
