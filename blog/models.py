from datetime import datetime

from django.db import models


class Category(models.Model):
    """A category for blog posts."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = u'categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.category', (), {'category_slug': self.slug})

class Post(models.Model):
    DRAFT = 0
    LIVE = 1
    HIDDEN = 2
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (LIVE, 'Live'),
        (HIDDEN, 'Hidden'),
    )

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=100, unique_for_date='pub_date')
    pub_date = models.DateTimeField(default=datetime.now,
        help_text='The post will not be made visible until this date (and '
        'still won\'t be visible unless set to Live)')
    byline = models.CharField(max_length=100)
    category = models.ForeignKey('Category')
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='uploads/blog_posts/', blank=True)
    body = models.TextField()

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.pub_date.strftime('%m/%d/%Y'))

    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.post', (), {
            'slug': self.slug,
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b'),
            'day': self.pub_date.day,
        })
