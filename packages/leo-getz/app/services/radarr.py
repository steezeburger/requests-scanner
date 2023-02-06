import json

import requests
import tmdbsimple as tmdb
from django.conf import settings
from requests.auth import HTTPBasicAuth

tmdb.API_KEY = settings.TMDB_TOKEN_V3
tmdb.REQUESTS_SESSION = requests.Session()


class Radarr:
    base_url = settings.RADARR_API_URL

    @classmethod
    def create_movie(cls, data: dict):
        endpoint = f'{cls.base_url}/movie'
        headers = {'content-type': 'application/json'}

        body = {
            'monitored': True,
            'minimumAvailability': 'announced',
            'addOptions': {
                'monitor': 'movieOnly',
                'searchForMovie': True,
                'addMethod': 'manual',
            },
            'qualityProfileId': settings.RADARR_QUALITY_PROFILE_ID,
            'rootFolderPath': settings.RADARR_ROOT_FOLDER_PATH,
            'tmdbid': data['tmdb_id'],
            'title': data['title'],
            'titleslug': data['title_slug'],
            'images': [{
                'coverType': 'poster',
                'url': data['full_poster_path'],
            }],
        }

        print(endpoint)
        res = requests.post(
            endpoint,
            auth=HTTPBasicAuth(settings.SEEDBOX_UN, settings.SEEDBOX_PW),
            params={'apiKey': settings.RADARR_API_KEY},
            data=json.dumps(body),
            headers=headers)

        print(res)
        data = res.json()
        print(data)

        return data
