from django.contrib import admin
from django.db import models

from galleries.admin import GalleryMediaInline
from products.models import Product, Tag


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
    list_display = ('name', 'num_products', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'slug', 'description', 'design',
                'related_info_1', 'related_info_2', 'related_info_3',
                'artists', 'tags',),
        }),
        ('Main Images', {
            'fields': ('main_image_1', 'main_image_2',),
        }),
        ('Payment Info', {
            'fields': ('status', 'price', 'min_quantity', 'max_quantity',
                'current_quantity',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts',),
            'classes': ('collapse',),
        })
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts', 'current_quantity',)
    filter_horizontal = ('artists', 'tags',)
    inlines = [GalleryMediaInline]
    list_display = ('name', 'price', 'current_quantity', 'status', 'created_ts',)
    list_filter = ('tags', 'status',)
    search_fields = ('name', 'description', 'design',)

admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)