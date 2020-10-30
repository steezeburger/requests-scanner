from django.contrib import admin

from .models import MovieRequest, PlexMovie


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


@admin.register(PlexMovie)
class PlexMovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'year',
        'created_at',
    )
    list_filter = (
        'created_at',
        'year',
    )
    search_fields = (
        'title',
        'year',
        'actors',
        'genres',
        'directors',
        'producers',
        'writers',
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'deleted_at', 'modified_at')
