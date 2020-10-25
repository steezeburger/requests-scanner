import os

from django.core.management import BaseCommand

from bot.bot import bot


class Command(BaseCommand):
    """
    Start the Discord bot server.
    """

    def handle(self, *args, **options):
        bot.run(os.environ['DISCORD_TOKEN'])
