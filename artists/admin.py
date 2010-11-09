from django.contrib import admin

from artists.models import Artist


class ArtistAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Artist Info', {
            'fields': ('name', 'slug', 'description', 'website', 'image',
                'order',),
        }),
        ('Metadata', {
            'fields': ('created_ts', 'updated_ts', 'is_active',),
            'classes': ('collapse',),
        })
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_ts', 'updated_ts',)
    list_display = ('name', 'order', 'website', 'is_active', 'created_ts',)
    list_filter = ('is_active',)
    search_fields = ('name', 'description',)

admin.site.register(Artist, ArtistAdmin)