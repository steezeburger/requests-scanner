from asgiref.sync import sync_to_async

from common.repositories.base_repository import BaseRepository
from movie_requests.models import PlexMovie


class PlexMovieRepository(BaseRepository):
    model = PlexMovie

    @classmethod
    def get_by_title(cls, title):
        plex_movie = cls.model.objects.filter(title__iexact=title).first()
        return plex_movie

    @classmethod
    @sync_to_async
    def get_by_title_async(cls, title):
        return cls.get_by_title(title)

    @classmethod
    def get_or_create(cls, data: dict):
        plex_movie = None

        if 'plex_guid' in data:
            qs = cls.model.objects.filter(
                plex_guid=data['plex_guid'])
            if qs:
                plex_movie = qs.first()

        if plex_movie is None:
            plex_movie = cls.model.objects.create(**data)

        return plex_movie
