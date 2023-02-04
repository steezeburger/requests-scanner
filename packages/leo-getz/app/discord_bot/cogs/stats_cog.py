import os
from functools import reduce
from typing import Tuple, Type

from asgiref.sync import sync_to_async
from discord import File
from discord.ext import commands
from discord.ext.commands import Context
from django.db.models import Count
from matplotlib import pyplot

from core.repositories.user_repository import UserRepository
from discord_bot.helpers import generate_size, partition
from movie_requests.repositories import MovieRequestRepository, PlexMovieRepository


class StatsCog(commands.Cog):
    def __init__(self,
                 bot,
                 repositories: Tuple[Type[UserRepository],
                                     Type[MovieRequestRepository],
                                     Type[PlexMovieRepository]]):
        self.bot = bot
        self.user_repository = repositories[0]
        self.movie_request_repository = repositories[1]
        self.plex_movie_repository = repositories[2]

    @commands.command(brief='Your stats',
                      help='Send !statsme to see stats about your movie requests.')
    async def statsme(self, ctx: 'Context'):
        author = ctx.author

        user = await self.user_repository.get_or_create_from_author_async(
            author)

        request_cnt = await sync_to_async(user.movierequests_created.count)()
        fulfilled_cnt = await sync_to_async(
            user.movierequests_created.filter(fulfilled=True).count
        )()

        await ctx.message.channel.send(
            f"{author.display_name} has requested {str(request_cnt)} movies.\n{fulfilled_cnt} have been fulfilled.")

    @commands.command(brief='Stats for the specified movie.',
                      usage='Name of Movie',
                      help='Send !statsmovie Some Movie to see how many times the movie has been requested.')
    async def statsmovie(self, ctx: 'Context', *args):
        movie_title = ' '.join(args)
        if not movie_title:
            await ctx.message.channel.send('You gotta pass in a movie name you dumb goof.')
            return

        movie_request = await MovieRequestRepository.get_by_title_async(movie_title)

        plex_movie = await PlexMovieRepository.get_by_title_async(movie_title)

        # build messages
        if not movie_request and not plex_movie:
            message = f'{movie_title} has not been requested, and it is not on the Plex server...\n'
            message += "probably because you haven't requested it."
        elif not movie_request and plex_movie:
            message = f'{plex_movie.title} has not been requested but I know what my guy likes, '
            message += f'and I added it to the Plex server on {plex_movie.created_at}'
        elif movie_request and not plex_movie:
            cnt = await movie_request.count_by_title_async
            message = f'{movie_request.movie_title} has been requested {str(cnt)} times.\n'
            message += 'Unfortunately it does not appear to be on the Plex server.'
        elif movie_request and plex_movie:
            cnt = await movie_request.count_by_title_async
            message = f'{movie_request.movie_title} has been requested {str(cnt)} times '
            message += f'and was added to the Plex server on {plex_movie.created_at}, because I love you'
        else:
            message = "What the fuck did you just say?"

        await ctx.message.channel.send(message)

    @commands.command(brief='Pie!',
                      help='A pie chart showing request count percentages.')
    async def statspie(self, ctx: 'Context'):
        request_counts = await sync_to_async(list)(
            UserRepository.model.objects.values(
                'nickname'
            ).annotate(
                r_count=Count('movierequests_created__movie_title')
            ).order_by('-r_count').all()
        )
        total_requests = await sync_to_async(
            self.movie_request_repository.model.objects.count)()

        if total_requests == 0:
            await ctx.message.channel.send("Sorry, I cannot generate a pie chart. There are no requests!\r\n"
                                           "DO YOU THINK I CAN DIVIDE BY ZERO?! FFS")
            return

        # grouping requests of < 10 into "others"
        top_request_counts, bottom_request_counts = partition(
            lambda x: x['r_count'] > 20, request_counts)

        combined_bottom_count = reduce(
            lambda acc, next_val: acc + next_val['r_count'],
            bottom_request_counts,
            0)
        combined_request_counts = top_request_counts + \
                                  [{'nickname': '...', 'r_count': combined_bottom_count}]

        labels = [
            f"{u['nickname']} ({u['r_count']})" for u in combined_request_counts]
        sizes = [generate_size(u['r_count'], total_requests)
                 for u in combined_request_counts]

        pyplot.clf()
        fig1, ax1 = pyplot.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')

        fig1.savefig('tmp.png')

        await ctx.send(file=File('tmp.png'))

        os.remove('tmp.png')
