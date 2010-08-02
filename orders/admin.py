from django.contrib import admin
from orders.models import Order, ProductInOrder


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0
    max_num = 0
    fields = ('product', 'quantity',)
    readonly_fields = ('product', 'quantity',)

class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Details', {
            'fields': ('session', 'status', 'created_ts', 'updated_ts',),
        }),
    )
    readonly_fields = ('session', 'status', 'created_ts', 'updated_ts',)
    inlines = [ProductInOrderInline]
    list_display = ('session', 'status', 'created_ts',)
    list_filter = ('status', 'created_ts',)

admin.site.register(Order, OrderAdmin)
