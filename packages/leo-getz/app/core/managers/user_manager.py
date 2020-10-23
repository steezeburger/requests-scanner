from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager used for creating users.
    """
    use_in_migrations = True

    def _create_user(self, nickname, password, **extra_fields):
        # email = self.normalize_email(email)
        if not nickname:
            raise ValueError('The nickname must be set')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, password=None, **extra_fields):
        """
        Creates and saves a :class:`User<core.models.User>`
        with the given nickname and password.

        :param nickname: :class:`python:str` or :func:`python:unicode`
            Nickname
        :param password: :class:`python:str` or :func:`python:unicode`
            Password
        :param extra_fields: :class:`python:dict`
            Additional pairs of attribute with value to be set on
            :class:`User<core.models.User>` instance.
        :return: Instance of created :class:`User<core.models.User>`
        :rtype: :class:`core.models.User`
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nickname, password, **extra_fields)

    def create_superuser(self, nickname, password, **extra_fields):
        """
        Creates and saves a :class:`User<core.models.User>`
        with the given nickname, password and superuser privileges.

        :param nickname: :class:`python:str`
            Nickname
        :param password: :class:`python:str`
            Password
        :param extra_fields: :class:`python:dict`
            Additional pairs of attribute with value to be set on
            :class:`User<core.models.User>` instance.
        :return: Instance of created :class:`User<core.models.User>`
        :rtype: :class:`core.models.User`
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(nickname, password, **extra_fields)
