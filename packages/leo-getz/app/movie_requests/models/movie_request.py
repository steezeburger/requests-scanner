from asgiref.sync import sync_to_async
from django.db import models
from django.utils.translation import gettext_lazy as _
from pgcrypto import fields

from common.models.created_by_mixin import CreatedByMixin
from common.models.encrypted_crud_timestamps_mixin import EncryptedCRUDTimestampsModelMixin
from common.models.soft_delete_timestamp_mixin import SoftDeleteTimestampMixin


class MovieRequest(CreatedByMixin,
                   SoftDeleteTimestampMixin,
                   EncryptedCRUDTimestampsModelMixin):
    """
    Model representing a request for a movie.
    """

    movie_title = fields.CharPGPSymmetricKeyField(
        max_length=255,
        db_index=True,
        help_text=_('The title of the movie.'))

    movie_url = fields.CharPGPSymmetricKeyField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('The URL for the movie.'))

    fulfilled = models.BooleanField(
        default=False,
        help_text=_('True if this request is fulfilled.'))

    movie = models.ForeignKey(
        'movie_requests.PlexMovie',
        related_name='movie_requests',
        on_delete=models.SET_NULL,
        null=True,
        help_text=_('The movie on the Plex server that fulfilled this request.'))

    class Meta:
        db_table = 'movie_requests'
        default_permissions = ()
        ordering = ('id',)

    @property
    def count_by_title(self):
        return MovieRequest.objects.filter(
            movie_title=self.movie_title).count()

    @property
    @sync_to_async
    def count_by_title_async(self):
        return self.count_by_title
