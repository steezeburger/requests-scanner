from django.test import TestCase

from core.test.helpers import UserFactory
from movie_requests.services import CreateMovieRequestService


class TestMovieRequestRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_should_create_movie_request(self):
        form = {
            'movie_title': 'The Title of the Movie',
            'movie_url': 'http://www.someurl.com',
            'nickname': self.user.nickname,
        }

        movie_request = CreateMovieRequestService.execute(form)

        self.assertEqual(form['movie_title'], movie_request.movie_title)
        self.assertEqual(form['movie_url'], movie_request.movie_url)
        self.assertEqual(self.user, movie_request.created_by)

        # not fulfilled by default
        self.assertEqual(False, movie_request.fulfilled)
