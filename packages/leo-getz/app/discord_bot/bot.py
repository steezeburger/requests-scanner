import os
from functools import reduce

from asgiref.sync import sync_to_async
from discord import File
from discord.ext import commands
from discord.ext.commands import Context
from django.db.models import Count
from matplotlib import pyplot

from discord_bot.helpers import partition, generate_size
from core.repositories.user_repository import UserRepository
from movie_requests.repositories import PlexMovieRepository
from movie_requests.repositories.movie_request_repository import MovieRequestRepository

MOVIE_DB_URL = 'themoviedb.org/movie'

bot = commands.Bot(command_prefix='!')


async def get_or_create_user_from_author(author):
    author_id = str(author.id)

    user_details = {
        'discord_id': author_id,
        'discord_username': author.name,
    }

    user = await UserRepository.get_or_create_async(data=user_details)

    return user


@bot.event
async def on_ready():
    print(f'Connected to Discord!')


@bot.command(pass_sontext=True,
             brief='Stats for the specified movie.',
             usage='Name of Movie',
             help='Send !moviestats Some Movie to see how many times the movie has been requested.')
async def moviestats(ctx: Context, *args):
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
        message += 'Unfortunately it does not appear to be on the Plex server. Go cry about it.'
    elif movie_request and plex_movie:
        cnt = await movie_request.count_by_title_async
        message = f'{movie_request.movie_title} has been requested {str(cnt)} times '
        message += f'and was added to the Plex server on {plex_movie.created_at}, because I love you'
    else:
        message = "What the fuck did you just say?"

    await ctx.message.channel.send(message)


@bot.command(pass_sontext=True,
             brief='Your stats',
             help='Send !stats to see stats about your movie requests.')
async def stats(ctx: Context):
    author = ctx.message.author

    user = await get_or_create_user_from_author(author)

    request_cnt = await sync_to_async(user.movierequests_created.count)()
    fulfilled_cnt = await sync_to_async(
        user.movierequests_created.filter(fulfilled=True).count
    )()

    await ctx.message.channel.send(
        f"{author.display_name} has requested {str(request_cnt)} movies.\n{fulfilled_cnt} have been fulfilled.")


@bot.command(pass_context=True,
             brief='Pie!',
             help='A pie chart showing request count percentages.')
async def statspie(ctx: Context):
    request_counts = await sync_to_async(list)(
        UserRepository.model.objects.values(
            'nickname'
        ).annotate(
            r_count=Count('movierequests_created__movie_title')
        ).order_by('-r_count').all()
    )
    total_requests = await sync_to_async(
        MovieRequestRepository.model.objects.count)()

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


@bot.event
async def on_message(message):
    is_request = MOVIE_DB_URL in message.content
    has_embed = len(message.embeds) > 0

    if is_request and has_embed:
        user = await get_or_create_user_from_author(message.author)
        embed = message.embeds[0]
        form = {
            'movie_title': embed.title,
            'movie_url': embed.url,
            'created_by': user,
        }
        await MovieRequestRepository.create_async(form)

@bot.event
async def on_message_edit(before, after):
    if len(before.embeds) == 0:
        return

    old_url = before.embeds[0].url
    url = after.embeds[0].url

    was_updated = not old_url and url and MOVIE_DB_URL in url
    if not was_updated:
        return

    # have to get this to determine who requested the movie
    prev_message_list = await after.channel.history(limit=2).flatten()
    prev_message = prev_message_list[1]
    author = prev_message.author

    user = await get_or_create_user_from_author(author)
    new_embed = after.embeds[0]
    form = {
        'movie_title': new_embed.title,
        'movie_url': new_embed.url,
        'created_by': user,
    }
    await MovieRequestRepository.create_async(form)

    # FIXME - will send a message when this is the only server running
    # await after.channel.send(
    #     f"{new_embed.title} will be coming right up...")
