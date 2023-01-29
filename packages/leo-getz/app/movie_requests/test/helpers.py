import factory

from factory.django import DjangoModelFactory

from movie_requests.models import PlexMovie
from movie_requests.models.movie_request import MovieRequest


class MovieRequestFactory(DjangoModelFactory):
    movie_title = factory.Faker('word')

    movie_url = factory.Faker('image_url')

    fulfilled = False

    class Meta:
        model = MovieRequest


class PlexMovieFactory(DjangoModelFactory):
    plex_guid = factory.Faker('uuid4')

    title = factory.Faker('bs')

    year = factory.Faker('year')

    duration = factory.Faker('unix_time')

    class Meta:
        model = PlexMovie
