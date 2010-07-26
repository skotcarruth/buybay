from django.contrib import admin
from django.db import models

from products.forms import AdminImageWidget
from products.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'slug', 'description', 'artists',),
        }),
        ('Payment Info', {
            'fields': ('price', 'offer_end',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        })
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    filter_horizontal = ('artists',)
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'offer_end', 'is_active', 'created_ts',)
    list_filter = ('offer_end', 'is_active',)
    search_fields = ('name', 'description',)

admin.site.register(Product, ProductAdmin)