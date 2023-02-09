import logging

from django.core.management import BaseCommand

from movie_requests.models import PlexMovie, MovieRequest

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Update requests' fulfilled property if the movie exists on the Plex server.
    """

    def handle(self, *args, **options):
        plex_movies = PlexMovie.objects.all()

        for movie in plex_movies:
            # FIXME - movie title is not a great way to find the exact same movie.
            #  can we either add PlexMovie.tmdb_id or maybe
            movie_requests = MovieRequest.objects.filter(
                movie_title=movie.title)

            if movie_requests.exists():
                logger.info(f'found {movie_requests.count()} requests for {movie.title}')

                movie_requests.update(
                    movie=movie,
                    fulfilled=True)
