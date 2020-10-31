from django.test import TestCase

from core.test.helpers import UserFactory
from movie_requests.repositories import PlexMovieRepository
from movie_requests.test.helpers import PlexMovieFactory


class TestPlexMovieRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_should_create_plex_movie(self):
        movie_details = {
            'plex_guid': 'abcd1234',
            'title': 'a title',
            'year': 1984,
            'duration': 124123123,
        }

        plex_movie = PlexMovieRepository.get_or_create(data=movie_details)

        self.assertEqual(movie_details['plex_guid'], plex_movie.plex_guid)
        self.assertEqual(movie_details['title'], plex_movie.title)
        self.assertEqual(movie_details['year'], plex_movie.year)
        self.assertEqual(movie_details['duration'], plex_movie.duration)

    def test_should_get_existing_plex_movie(self):
        plex_movie = PlexMovieFactory()

        movie_details = {
            'plex_guid': plex_movie.plex_guid,
        }
        obj_from_db = PlexMovieRepository.get_or_create(
            data=movie_details)

        self.assertEqual(plex_movie.pk, obj_from_db.pk)

    def test_should_get_plex_movie_by_title_iexact(self):
        plex_movie = PlexMovieFactory(title='BANANA')

        obj_from_db = PlexMovieRepository.get_by_title(
            plex_movie.title.lower())

        self.assertEqual(plex_movie.title, obj_from_db.title)