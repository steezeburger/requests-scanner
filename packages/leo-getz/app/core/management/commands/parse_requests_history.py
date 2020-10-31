import datetime
import os

import pytz
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from core.repositories.user_repository import UserRepository
from movie_requests.repositories.movie_request_repository import MovieRequestRepository

""" 
Selectors 
"""

message_content_selector = \
    'div.chatlog__messages > div.chatlog__message > div.chatlog__content > div.markdown'

message_author_selector = \
    'div.chatlog__messages > span.chatlog__author-name'

embed_path = \
    'div.chatlog__messages > div.chatlog__message > div.chatlog__embed'

movie_title_path = \
    'div.chatlog__messages > div.chatlog__message > div.chatlog__embed > div.chatlog__embed-content-container > ' + \
    'div.chatlog__embed-content > div.chatlog__embed-text > div.chatlog__embed-title > a.chatlog__embed-title-link > ' + \
    'div.markdown'

movie_url_path = \
    'div.chatlog__messages > div.chatlog__message > div.chatlog__embed > div.chatlog__embed-content-container > ' + \
    'div.chatlog__embed-content > div.chatlog__embed-text > div.chatlog__embed-title > a.chatlog__embed-title-link'

timestamp_path = \
    'div.chatlog__messages > span.chatlog__timestamp'


class Command(BaseCommand):
    """
    Parse the requests channel history.
    """

    def handle(self, *args, **options):
        history_file = open(
            'core/management/commands/data/requests_history.html',
            'r')

        try:

            contents = history_file.read()
            soup = BeautifulSoup(contents, 'lxml')

            message_elements = soup.find_all('div', {'class': 'chatlog__message-group'})

            requests = []
            for elem in message_elements:
                message_content = elem.select_one(message_content_selector)
                if message_content and message_content.text.startswith('.movie '):
                    # NOTE - we have a movie request message

                    # get author information
                    author_elem = elem.select_one(message_author_selector)
                    author_discord_id = author_elem['data-user-id']
                    author_discord_username = author_elem['title'].split('#')[0]
                    author_nickname = author_elem.text

                    author_details = {
                        'discord_id': author_discord_id,
                        'discord_username': author_discord_username,
                    }

                    sibling_movie_message = elem.find_next_sibling('div')

                    embed_elem = sibling_movie_message.select_one(embed_path)
                    if embed_elem:
                        movie_title_elem = embed_elem.select_one(movie_title_path)
                        movie_url_elem = embed_elem.select_one(movie_url_path)

                        if movie_title_elem and movie_url_elem:
                            # NOTE - we have a matching embed with title and url

                            # ex of timestamp_str format 17-Jun-20 12:08 AM
                            # %d-%b-%y %I:%M %p
                            timestamp_elem = sibling_movie_message.select_one(timestamp_path)
                            timestamp_str = timestamp_elem.text
                            timestamp_obj = datetime.datetime.strptime(timestamp_str, '%d-%b-%y %I:%M %p')

                            user = UserRepository.get_or_create(data=author_details)

                            movie_request_details = {
                                'movie_title': movie_title_elem.text,
                                'movie_url': movie_url_elem['href'],
                                'created_by': user,
                            }

                            movie_request = MovieRequestRepository.create(movie_request_details)
                            movie_request.created_at = timestamp_obj
                            movie_request.save()

                            print('####')
                            print(message_content.text)
                            print(movie_request_details)

                            requests.append(elem)

            print(len(requests))
        finally:
            history_file.close()
