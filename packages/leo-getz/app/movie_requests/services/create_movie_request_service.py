from django import forms
from service_objects.services import Service

from core.repositories.user_repository import UserRepository
from movie_requests.models import MovieRequest
from movie_requests.repositories.movie_request_repository import MovieRequestRepository


class CreateMovieRequestService(Service):
    """
    Create a MovieRequest, and the User if they do not exist.
    """

    movie_title = forms.CharField()

    movie_url = forms.URLField()

    discord_username = forms.CharField(required=False)

    discord_id = forms.CharField(required=False)

    def process(self) -> 'MovieRequest':
        form = self.cleaned_data

        user_details = {
            'discord_id': form.pop('discord_id'),
            'discord_username': form.pop('discord_username'),
        }
        user = UserRepository.get_or_create(data=user_details)

        form['created_by'] = user

        movie_request = MovieRequestRepository.create(form)
        return movie_request

    def post_process(self):
        # TODO - send discord message back
        pass
