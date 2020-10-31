from django.test import TestCase

from core.repositories.user_repository import UserRepository
from core.test.helpers import UserFactory


class TestUserRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_should_create_user(self):
        user_details = {
            'nickname': '_The Architect_',
            'discord_id': 'abcd1234',
            'discord_username': 'steezeburger',
        }

        user = UserRepository.get_or_create(data=user_details)

        self.assertEqual(user_details['nickname'], user.nickname)
        self.assertEqual(user_details['discord_id'], user.discord_id)
        self.assertEqual(user_details['discord_username'], user.discord_username)

    def test_should_create_user_set_nickname_as_discord_username(self):
        user_details = {
            'discord_id': 'abcd1234',
            'discord_username': 'steezeburger',
        }

        user = UserRepository.get_or_create(data=user_details)

        self.assertEqual(user_details['nickname'], user.discord_username)

    def test_should_get_existing_user(self):
        user = UserFactory()

        user_details = {
            'nickname': user.nickname,
            'discord_id': user.discord_id,
            'discord_username': user.discord_username,
        }
        obj_from_db = UserRepository.get_or_create(
            data=user_details)

        self.assertEqual(user.pk, obj_from_db.pk)
