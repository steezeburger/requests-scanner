from django.test import TestCase

from core.test.helpers import UserFactory
from movie_requests.repositories.movie_request_repository import MovieRequestRepository


class TestMovieRequestRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_should_create_movie_request(self):
        details = {
            'movie_title': 'The Title of the Movie',
            'movie_url': 'http://www.someurl.com',
            'fulfilled': False,
            'created_by': self.user,
        }

        movie_request = MovieRequestRepository.create(details)

        self.assertEqual(details['movie_title'], movie_request.movie_title)
        self.assertEqual(details['movie_url'], movie_request.movie_url)
        self.assertEqual(details['fulfilled'], movie_request.fulfilled)
