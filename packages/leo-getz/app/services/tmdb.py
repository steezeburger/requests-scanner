import requests
import tmdbsimple as tmdb
from django.conf import settings

tmdb.API_KEY = settings.TMDB_TOKEN_V3
tmdb.REQUESTS_SESSION = requests.Session()


class TMDB:
    @classmethod
    def get_movie_by_id(cls, tmdb_id: int):
        movie = tmdb.Movies(tmdb_id)
        response = movie.info()
        return response
