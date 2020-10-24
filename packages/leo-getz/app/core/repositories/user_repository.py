from common.repositories.base_repository import BaseRepository
from core.models import User


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def create(cls, data: dict) -> 'User':
        user = cls.model.objects.create(**data)
        return user

    @classmethod
    def get_or_create(cls, *, nickname: str):
        user = cls.get_by_nickname(nickname)

        if not user:
            user = cls.create({'nickname': nickname})

        return user

    @classmethod
    def get_by_nickname(cls, nickname):
        try:
            user = cls.model.objects.get(nickname=nickname)
        except cls.model.DoesNotExist:
            return None

        return user
