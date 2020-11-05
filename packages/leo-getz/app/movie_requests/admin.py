from django import forms
from django.contrib import admin

from .models import MovieRequest, PlexMovie


class MovieRequestAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].required = False

    class Meta:
        model = MovieRequest
        fields = '__all__'


@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    form = MovieRequestAdminForm
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
