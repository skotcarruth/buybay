from datetime import datetime

from django.contrib.contenttypes import generic
from django.db import models

from galleries.models import GalleryMedia


class TagManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Tag(models.Model):
    """A category for blog posts."""
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
        return ('blog.views.tag', (), {'tag_slug': self.slug})

    def num_posts(self):
        return self.post_set.count()
    num_posts.short_description = 'Posts'

class PostManager(models.Manager):
    def active(self):
        return self.filter(status=Post.LIVE, pub_date__lte=datetime.now())

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
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    tags = models.ManyToManyField('Tag', blank=True)

    tease = models.TextField(blank=True)
    body = models.TextField()

    gallery_media = generic.GenericRelation(GalleryMedia)

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    objects = PostManager()

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
