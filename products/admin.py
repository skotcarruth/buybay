from django.contrib import admin

from products.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'slug', 'description',),
        }),
        ('Payment Info', {
            'fields': ('price', 'offer_end',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        })
    )
    list_display = ('name', 'price', 'offer_end', 'is_active',)
    list_filter = ('offer_end', 'is_active',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    search_fields = ('name', 'description',)
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)