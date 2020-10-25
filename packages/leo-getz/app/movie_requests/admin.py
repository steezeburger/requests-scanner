from django.contrib import admin

from .models import MovieRequest


@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'movie_title',
        'fulfilled',
        'created_at',
        'created_by',
    )
    list_filter = (
        'created_by',
        'created_at',
        'fulfilled',
    )
    search_fields = ('movie_title', 'movie_url')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'deleted_at', 'modified_at')
