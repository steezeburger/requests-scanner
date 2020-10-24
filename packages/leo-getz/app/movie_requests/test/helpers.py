import factory

from factory.django import DjangoModelFactory

from movie_requests.models.movie_request import MovieRequest


class MovieRequestFactory(DjangoModelFactory):
    movie_title = factory.Faker('word')

    movie_url = factory.Faker('image_url')

    fulfilled = False

    class Meta:
        model = MovieRequest
