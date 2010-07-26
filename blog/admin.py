from django.contrib import admin
from django.db import models

from widgets import AdminImageWidget
from blog.models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Category Info', {
            'fields': ('name', 'slug',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'byline', 'category', 'pub_date', 'status',),
        }),
        ('Post Body', {
            'fields': ('body', 'image',),
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
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    list_display = ('title', 'pub_date', 'category', 'status',)
    list_filter = ('pub_date', 'category', 'status',)
    search_fields = ('title', 'byline', 'body',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
