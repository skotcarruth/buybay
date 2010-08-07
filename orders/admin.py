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
        ('PayPal Buyer Details', {
            'fields': ('user_email', 'user_salutation', 'user_firstname',
                'user_middlename', 'user_lastname', 'user_suffix',
                'user_shiptoname', 'user_shiptostreet', 'user_shiptostreet2',
                'user_shiptocity', 'user_shiptostate', 'user_shiptozip',
                'user_shiptocountrycode', 'user_shiptophonenum',),
        }),
        ('PayPal Payment Details', {
            'fields': ('paypal_transactionid', 'paypal_ordertime',
                'paypal_paymentstatus', 'paypal_paymenttype', 'paypal_amt',
                'paypal_feeamt',),
        })
    )
    readonly_fields = ('id', 'status', 'created_ts', 'user_email',
        'user_salutation', 'user_firstname', 'user_middlename',
        'user_lastname', 'user_suffix', 'user_shiptoname',
        'user_shiptostreet', 'user_shiptostreet2', 'user_shiptocity',
        'user_shiptostate', 'user_shiptozip', 'user_shiptocountrycode',
        'user_shiptophonenum', 'paypal_transactionid', 'paypal_ordertime',
        'paypal_paymentstatus', 'paypal_paymenttype', 'paypal_amt',
        'paypal_feeamt',)
    inlines = [ProductInOrderInline]
    list_display = ('id', 'status', 'get_total_items', 'get_total_price_display', 'created_ts',)
    list_filter = ('status', 'created_ts',)

admin.site.register(Order, OrderAdmin)
