from common.repositories.base_repository import BaseRepository
from movie_requests.models import PlexMovie


class PlexMovieRepository(BaseRepository):
    model = PlexMovie

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
