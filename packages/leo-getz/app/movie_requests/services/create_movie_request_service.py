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

    nickname = forms.CharField()

    def process(self) -> 'MovieRequest':
        nickname = self.cleaned_data.pop('nickname')

        user = UserRepository.get_or_create(nickname=nickname)

        self.cleaned_data['created_by'] = user

        movie_request = MovieRequestRepository.create(self.cleaned_data)
        return movie_request

    def post_process(self):
        # TODO - send discord message back
        pass
