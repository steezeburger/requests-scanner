from asgiref.sync import sync_to_async

from common.repositories.base_repository import BaseRepository
from movie_requests.models import MovieRequest


class MovieRequestRepository(BaseRepository):
    model = MovieRequest

    @classmethod
    def get_by_filter(cls, filter_input: dict = None):
        if filter_input:
            movie_requests = cls.get_queryset().filter(**filter_input)
        else:
            movie_requests = cls.get_queryset().all()
        return movie_requests

    @classmethod
    def create(cls, data: dict) -> 'MovieRequest':
        movie_request = cls.model.objects.create(**data)
        return movie_request

    @classmethod
    @sync_to_async
    def create_async(cls, data: dict) -> 'MovieRequest':
        return cls.create(data)

    @classmethod
    def delete(cls, *, pk=None, obj: 'MovieRequest' = None) -> 'MovieRequest':
        movie_request = obj or cls.get(pk=pk)
        movie_request.delete()
        return movie_request

    @classmethod
    def get_by_title(cls, title: str) -> 'MovieRequest':
        return cls.model.objects.filter(
            movie_title__iexact=title).first()

    @classmethod
    @sync_to_async
    def get_by_title_async(cls, title: str):
        return cls.get_by_title(title)

    @classmethod
    def get_by_tmdb_id(cls, tmdb_id: int) -> 'MovieRequest':
        return cls.model.objects.filter(
            tmdb_id=tmdb_id).first()

    @classmethod
    @sync_to_async
    def get_by_tmdb_id_async(cls, tmdb_id: int):
        return cls.get_by_tmdb_id(tmdb_id)

    @classmethod
    def update(cls, *, pk=None, obj: 'MovieRequest' = None, data: dict) -> 'MovieRequest':
        movie_request = obj or cls.get(pk=pk)

        if data.get('movie_title'):
            movie_request.movie_title = data['movie_title']

        if data.get('movie_url'):
            movie_request.movie_url = data['movie_url']

        if data.get('fulfilled'):
            movie_request.fulfilled = data['fulfilled']

        movie_request.save()
        return movie_request
