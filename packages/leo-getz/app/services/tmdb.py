import requests
import tmdbsimple as tmdb
from django.conf import settings

tmdb.API_KEY = settings.TMDB_TOKEN_V3
tmdb.REQUESTS_SESSION = requests.Session()


class TMDB:
    poster_base_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'

    @classmethod
    def get_movie_by_id(cls, tmdb_id: int):
        movie = tmdb.Movies(tmdb_id)
        response = movie.info()
        return response

    @classmethod
    def get_poster_full_path(cls, poster_path) -> str:
        return f'{cls.poster_base_url}{poster_path}'
