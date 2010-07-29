from django.contrib import admin
from django.db import models

from galleries.widgets import AdminImageWidget
from features.models import Feature


class FeatureAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Feature Info', {
            'fields': ('product', 'image_before', 'image_after', 'order', 'link_override',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_ts', 'updated_ts',)
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    list_display = ('product', 'order', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active',)

admin.site.register(Feature, FeatureAdmin)
