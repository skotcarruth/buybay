from django.db import models


class Page(models.Model):
    """A page of flat content on the site."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/flatpage_images/', blank=True)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.slug

class Blurb(models.Model):
    """A blurb of text on the site."""
    slug = models.SlugField(unique=True, help_text=u'This describes the '
        'position on the site where this blurb goes. Do NOT change this '
        'unless you\'re sure you know what you\'re doing. Please only use '
        'letters, numbers, underscores or hyphens.')
    content = models.TextField()

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return self.slug
