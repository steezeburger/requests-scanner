import random
import stringcase

from services.tmdb import TMDB


def partition(pred, iterable):
    """
    Partitions an iterable into two lists based on pred (predicate).
    """

    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses


def generate_size(count, total):
    """
    Generates a percentage w/ 2 decimal places.
    """

    percentage = count / total * 100
    return round(percentage, 2)


def get_random_affirm(title: str) -> str:
    """
    Return a random response for affirmations.
    """

    messages = [
        f"{title} will be coming right up!",
        f"All right all right, I'm gettin' to it! {title} will be on the Plex in a bit.",
        f"How bout you's just hold ya horses eh? {title} will be downloaded in a minute!",
    ]

    message = random.choice(messages)
    return message

def get_radarr_request_from_tmdb_info(tmdb_info: dict) -> dict:
    """
    Converts a dictionary from a tmdb response into a dictionary that can
    be sent to Radarr's API
    """

    tmdb_id = tmdb_info.get('id')
    title = tmdb_info.get('title')
    title_slug = f'{stringcase.snakecase(title)}-{tmdb_id}'
    full_poster_path = TMDB.get_poster_full_path(tmdb_info.get('poster_path'))

    return {
        'tmdb_id': tmdb_id,
        'title': title,
        'title_slug': title_slug,
        'full_poster_path': full_poster_path
    }