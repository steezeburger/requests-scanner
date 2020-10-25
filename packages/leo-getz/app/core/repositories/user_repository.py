from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError

from common.repositories.base_repository import BaseRepository
from core.models import User


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def create(cls, data: dict) -> 'User':
        user = cls.model.objects.create(**data)
        return user

    @classmethod
    @sync_to_async
    def get_or_create(cls, *, data: dict):
        if 'discord_id' not in data or 'discord_username' not in data:
            raise ValidationError("Input must include `discord_id` or `discord_username`")

        user = None
        if 'discord_id' in data:
            user = cls.get_by_discord_id(data['discord_id'])
        if 'discord_username' in data:
            user = cls.get_by_discord_username(data['discord_username'])

        if not user:
            if 'nickname' not in data:
                data['nickname'] = data.get('discord_username') or data.get('discord_id')
            user = cls.create(data)

        return user

    @classmethod
    def get_by_discord_id(cls, discord_id):
        try:
            user = cls.model.objects.get(discord_id=discord_id)
        except cls.model.DoesNotExist:
            return None

        return user

    @classmethod
    def get_by_discord_username(cls, discord_username):
        try:
            user = cls.model.objects.get(discord_username=discord_username)
        except cls.model.DoesNotExist:
            return None

        return user
