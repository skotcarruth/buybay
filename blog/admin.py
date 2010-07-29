from django.contrib import admin
from django.db import models

from blog.models import Post, Tag
from galleries.admin import GalleryMediaInline


class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Tag Info', {
            'fields': ('name', 'slug',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    list_display = ('name', 'num_posts', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'byline', 'pub_date', 'status', 'tags',),
        }),
        ('Post Body', {
            'fields': ('tease', 'body',),
            'description': 'For the post body, you may use Textile to do '
                'basic HTML formatting like italics and creating links. '
                '(<a href="http://textile.thresholdstate.com/">Textile reference</a>)',
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts',),
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    filter_horizontal = ('tags',)
    inlines = [GalleryMediaInline]
    list_display = ('title', 'pub_date', 'status',)
    list_filter = ('pub_date', 'status',)
    search_fields = ('title', 'byline', 'body',)

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
