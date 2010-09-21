import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse

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
        }),
        ('Donation Options', {
            'fields': ('donation',),
        }),
    )
    readonly_fields = ('id', 'status', 'created_ts', 'user_email',
        'user_salutation', 'user_firstname', 'user_middlename',
        'user_lastname', 'user_suffix', 'user_shiptoname',
        'user_shiptostreet', 'user_shiptostreet2', 'user_shiptocity',
        'user_shiptostate', 'user_shiptozip', 'user_shiptocountrycode',
        'user_shiptophonenum', 'paypal_transactionid', 'paypal_ordertime',
        'paypal_paymentstatus', 'paypal_paymenttype', 'paypal_amt',
        'paypal_feeamt', 'donation',)
    inlines = [ProductInOrderInline]
    list_display = ('id', 'status', 'get_total_items', 'get_total_price_display', 'created_ts',)
    list_filter = ('status', 'created_ts',)
    actions = ['export_orders_to_csv']

    def export_orders_to_csv(self, request, queryset):
        """Exports the selected orders to a CSV file for download."""
        # Initialize the response and CSV writer
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'
        writer = csv.writer(response)

        # Write the data to CSV
        writer.writerow(['Buy the Bay Orders'])
        writer.writerow(['Generated: %s' % datetime.utcnow().date().strftime('%m/%d/%Y')])
        writer.writerow([])
        writer.writerow(['ID', 'Date', 'Order Status', 'Products', 'Total',
            'Email', 'First Name', 'Last Name', 'Phone', 'City', 'State',
            'ZIP', 'PayPal Transaction ID',])
        for order in queryset:
            writer.writerow([
                order.id,
                order.paypal_ordertime.strftime('%m/%d/%Y %H:%M') if order.paypal_ordertime else '',
                order.get_status_display(),
                ', '.join([product.name for product in order.products.all()]),
                str(order.paypal_amt),
                order.user_email,
                order.user_firstname,
                order.user_lastname,
                order.user_shiptophonenum,
                order.user_shiptocity,
                order.user_shiptostate,
                order.user_shiptozip,
                order.paypal_transactionid,
            ])

        # Return the CSV
        return response
    export_orders_to_csv.short_description = 'Export to CSV'

admin.site.register(Order, OrderAdmin)
