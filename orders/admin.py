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
            'fields': ('id', 'status', 'created_ts',),
        }),
    )
    readonly_fields = ('id', 'status', 'created_ts',)
    inlines = [ProductInOrderInline]
    list_display = ('id', 'status', 'get_total_items', 'get_total_price_display', 'created_ts',)
    list_filter = ('status', 'created_ts',)

admin.site.register(Order, OrderAdmin)
