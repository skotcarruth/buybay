from django.db import models


class Artist(models.Model):
    """An artist who makes the products."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    website = models.URLField(verify_exists=False)
    image = models.ImageField(upload_to='uploads/artist_images/')

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_ts']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('artists.views.artist', (), {'artist_slug': self.slug})

    def active_products(self):
        return self.product_set.active()
