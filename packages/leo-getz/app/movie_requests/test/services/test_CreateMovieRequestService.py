from django.test import TestCase

from core.test.helpers import UserFactory
from movie_requests.services import CreateMovieRequestService


class TestMovieRequestRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            nickname='pumpkin',
            discord_id='asdf',
            discord_username='pumpkin')

    def test_should_create_movie_request(self):
        form = {
            'movie_title': 'The Title of the Movie',
            'movie_url': 'http://www.someurl.com',
            'discord_username': self.user.nickname,
            'discord_id': self.user.discord_id,
        }

        movie_request = CreateMovieRequestService.execute(form)

        self.assertEqual(form['movie_title'], movie_request.movie_title)
        self.assertEqual(form['movie_url'], movie_request.movie_url)
        self.assertEqual(self.user, movie_request.created_by)

        # not fulfilled by default
        self.assertEqual(False, movie_request.fulfilled)

    def test_should_create_movie_request_and_user(self):
        form = {
            'movie_title': 'The Title of the Movie',
            'movie_url': 'http://www.someurl.com',
            'discord_username': 'discord_paul',
            'discord_id': 'ABCD-1234',
        }

        movie_request = CreateMovieRequestService.execute(form)

        self.assertEqual(form['movie_title'], movie_request.movie_title)
        self.assertEqual(form['movie_url'], movie_request.movie_url)

        # did create user properly
        self.assertEqual(form['discord_id'],
                         movie_request.created_by.discord_id)
        self.assertEqual(form['discord_username'],
                         movie_request.created_by.discord_username)
        # did set user nickname to discord_username
        self.assertEqual(form['discord_username'],
                         movie_request.created_by.nickname)

        # not fulfilled by default
        self.assertEqual(False, movie_request.fulfilled)
