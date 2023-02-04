import random


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
