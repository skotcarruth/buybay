from django.contrib import admin

from galleries.admin import GalleryMediaInline
from products.models import Product, Tag, ProductComment


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
                'artists', 'tags', 'order',),
        }),
        ('Main Images', {
            'fields': ('name_image', 'main_image_1', 'main_image_2',),
        }),
        ('Payment Info', {
            'fields': ('status', 'price', 'tax_deductible', 'min_quantity',
                'max_quantity', 'current_quantity',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts',),
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    filter_horizontal = ('artists', 'tags',)
    inlines = [GalleryMediaInline]
    list_display = ('name', 'order', 'price', 'current_quantity', 'status', 'created_ts',)
    list_filter = ('tags', 'status',)
    search_fields = ('name', 'description', 'design',)

class ProductCommentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Comment Info', {
            'fields': ('product', 'name', 'thumb_url', 'comment',),
        }),
        ('Metadata', {
            'fields': ('is_active', 'created_ts', 'updated_ts',),
        }),
    )
    readonly_fields = ('created_ts', 'updated_ts', 'product', 'name', 'thumb_url', 'comment',)
    list_display = ('product', 'name', 'is_active', 'created_ts',)
    list_filter = ('is_active', 'created_ts',)
    search_fields = ('name', 'comment',)

admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
