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
    def get_or_create(cls, *, data: dict):
        if 'discord_id' not in data and 'discord_username' not in data:
            raise ValidationError("Input must include `discord_id` or `discord_username`")

        user = None
        if 'discord_id' in data:
            user = cls.get_by_discord_id(data['discord_id'])
        if not user and 'discord_username' in data:
            user = cls.get_by_discord_username(data['discord_username'])

        if not user:
            if 'nickname' not in data:
                data['nickname'] = data.get('discord_username') or data.get('discord_id')
            user = cls.create(data)

        return user

    @classmethod
    async def get_or_create_from_author_async(cls, author):
        author_id = str(author.id)

        user_details = {
            'discord_id': author_id,
            'discord_username': author.name,
        }

        user = await cls.get_or_create_async(
            data=user_details)

        return user

    @classmethod
    @sync_to_async
    def get_or_create_async(cls, *, data: dict):
        return cls.get_or_create(data=data)

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
