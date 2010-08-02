from django.contrib import admin

from flatcontent.models import Blurb, Page


class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Page Info', {
            'fields': ('name', 'slug', 'image', 'content',),
            'description': 'For the content, you may use Textile to do '
                'basic HTML formatting like italics and creating links. '
                '(<a href="http://textile.thresholdstate.com/">Textile reference</a>)',
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    list_display = ('name', 'is_active', 'created_ts',)
    list_filter = ('is_active',)
    search_fields = ('name', 'content',)

class BlurbAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Blurb Info', {
            'fields': ('content',),
            'description': 'For the content, you may use Textile to do '
                'basic HTML formatting like italics and creating links. '
                '(<a href="http://textile.thresholdstate.com/">Textile reference</a>)',
        }),
        ('Metadata', {
            'fields': ('slug', 'created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_ts', 'updated_ts',)
    list_display = ('slug', 'is_active', 'created_ts',)
    list_filter = ('is_active',)
    search_fields = ('content',)

admin.site.register(Page, PageAdmin)
admin.site.register(Blurb, BlurbAdmin)
