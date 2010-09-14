from django.contrib import admin

from mail.models import Message


class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Email Message', {
            'fields': ('to_email', 'from_email', 'subject', 'body_text',
                'body_html',),
        }),
        ('Delivery Info', {
            'fields': ('sent', 'sent_ts', 'created_ts',
                'failed_send_attempts', 'max_send_attempts',),
        }),
        ('Logs', {
            'fields': ('logs',),
        }),
    )
    readonly_fields = ('to_email', 'from_email', 'subject', 'body_text',
        'body_html', 'sent', 'sent_ts', 'scheduled_delivery', 'created_ts',
        'failed_send_attempts', 'max_send_attempts', 'logs',)
    list_display = ('subject', 'to_email', 'created_ts', 'sent',)
    list_filter = ('sent', 'sent_ts', 'created_ts',)

admin.site.register(Message, MessageAdmin)
