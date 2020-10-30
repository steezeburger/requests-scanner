from plexapi.myplex import MyPlexAccount

from django.conf import settings
from django.core.management import BaseCommand

from movie_requests.repositories.plex_movie_repository import PlexMovieRepository


class Command(BaseCommand):
    """
    Sync Leo's database with the movies on the Plex.
    """

    def handle(self, *args, **options):
        account = MyPlexAccount(settings.PLEX_USERNAME,
                                settings.PLEX_PASSWORD)
        plex = account.resource('lw817-iceburgs').connect()

        movies = plex.library.section('Movies')

        # TODO - sort by addedAt and only fetch last day or two
        # TODO - schedule this job to run every night
        for movie in movies.all(sort='titleSort'):
            movie_details = {
                'plex_guid': movie.guid,
                'title': movie.title,
                'year': movie.year,
                'duration': movie.duration,
                'actors': [t.tag for t in movie.actors],
                'genres': [t.tag for t in movie.genres],
                'directors': [t.tag for t in movie.directors],
                'producers': [t.tag for t in movie.producers],
                'writers': [t.tag for t in movie.writers],
            }
            plex_movie = PlexMovieRepository.get_or_create(movie_details)

            plex_movie.created_at = movie.addedAt
            plex_movie.save()

            # TODO - find matching request if exists and update fulfilled status
