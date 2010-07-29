from django.contrib.contenttypes import generic
from django.db import models

from galleries.widgets import AdminImageWidget
from galleries.models import GalleryMedia


class GalleryMediaInline(generic.GenericTabularInline):
    model = GalleryMedia
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    extra = 0
