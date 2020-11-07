from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.crud_timestamps_mixin import CRUDTimestampsMixin
from common.models.soft_delete_timestamp_mixin import SoftDeleteTimestampMixin


class PlexMovie(SoftDeleteTimestampMixin,
                CRUDTimestampsMixin):
    """
    Model representing a movie that exists on the Plex server.
    """

    plex_guid = models.CharField(
        max_length=512,
        help_text=_('Plex GUID.'))

    title = models.CharField(
        max_length=255,
        help_text=_('The title of the movie.'))

    year = models.SmallIntegerField(
        db_index=True,
        null=True,
        blank=True,
        help_text=_('The year the movie was released.'))

    duration = models.BigIntegerField(
        help_text=_('The duration of the movie in milliseconds.'))

    actors = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True)

    genres = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True)

    directors = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True)

    producers = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True)

    writers = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True)

    class Meta:
        db_table = 'plex_movies'
        default_permissions = ()
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} ({self.year})'
