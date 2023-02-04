from django.test import TestCase

from core.test.helpers import UserFactory
from movie_requests.repositories.movie_request_repository import MovieRequestRepository
from movie_requests.test.helpers import MovieRequestFactory


class TestMovieRequestRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_should_create_movie_request(self):
        details = {
            'movie_title': 'The Title of the Movie',
            'movie_url': 'http://www.someurl.com',
            'tmdb_id': 603,
            'fulfilled': False,
            'created_by': self.user,
        }

        movie_request = MovieRequestRepository.create(details)

        self.assertEqual(details['movie_title'], movie_request.movie_title)
        self.assertEqual(details['movie_url'], movie_request.movie_url)
        self.assertEqual(details['fulfilled'], movie_request.fulfilled)

    def test_should_get_movie_request_count_by_title(self):
        movie_request = MovieRequestFactory(
            movie_title='banana',
            movie_url='www.google.com',
            tmdb_id=603,
            fulfilled=False,
            created_by=self.user)
        movie_request_2 = MovieRequestFactory(
            movie_title='banana',
            movie_url='www.google.com',
            tmdb_id=604,
            fulfilled=False,
            created_by=self.user)

        obj_from_db = MovieRequestRepository.get_by_title(
            movie_request.movie_title)

        self.assertEqual(2, obj_from_db.count_by_title)
