from django.contrib import admin

from paypal.models import IPNRecord


class IPNRecordAdmin(admin.ModelAdmin):
    fields = ('transaction_id', 'data', 'created_ts',)
    readonly_fields = ('transaction_id', 'data', 'created_ts',)
    list_display = ('transaction_id', 'created_ts',)

admin.site.register(IPNRecord, IPNRecordAdmin)
