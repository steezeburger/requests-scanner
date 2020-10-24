import factory
from factory.django import DjangoModelFactory

from core.models import User

TEST_PASSWORD = 'password123'


class UserFactory(DjangoModelFactory):
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)

    nickname = factory.Faker('user_name')

    is_active = True
    is_staff = False

    class Meta:
        model = User
