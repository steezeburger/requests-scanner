import os
from functools import reduce

from asgiref.sync import sync_to_async
from discord import File
from discord.ext import commands
from discord.ext.commands import Context
from django.db.models import Count
from matplotlib import pyplot

from bot.helpers import partition
from core.repositories.user_repository import UserRepository
from movie_requests.repositories.movie_request_repository import MovieRequestRepository

bot = commands.Bot(command_prefix='!')


async def get_or_create_user_from_author(author):
    author_id = str(author.id)

    user_details = {
        'discord_id': author_id,
        'discord_username': author.name,
    }

    user = await UserRepository.get_or_create(data=user_details)

    return user


@bot.command(pass_sontext=True,
             brief='Stats for the movie specified',
             usage='Name of Movie',
             help='Send !moviestats Some Movie to see how many times the movie has been requested.')
async def moviestats(ctx: Context, *args):
    movie_title = ' '.join(args)
    movie_requests = await sync_to_async(list)(MovieRequestRepository.model.objects.filter(
        movie_title__iexact=movie_title).all())

    cnt = len(movie_requests)

    if cnt > 0:
        await ctx.message.channel.send(
            f"{movie_requests[0].movie_title} has been requested {str(cnt)} times.")
    else:
        await ctx.message.channel.send(
            f"{movie_title} has not been requested.")


@bot.command(pass_sontext=True,
             brief='Your stats',
             help='Send !stats to see stats about your movie requests.')
async def stats(ctx: Context):
    author = ctx.message.author

    user = await get_or_create_user_from_author(author)

    cnt = await sync_to_async(user.movierequests_created.count)()

    await ctx.message.channel.send(
        f"{author.display_name} has requested {str(cnt)} movies.")


@bot.command(pass_context=True,
             brief='Pie!',
             help='A pie chart showing request count percentages.')
async def statspie(ctx: Context):
    def generate_size(count, total):
        percentage = count / total * 100
        return round(percentage, 2)

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
    combined_request_counts = top_request_counts + [{'nickname': 'Others', 'r_count': combined_bottom_count}]

    labels = [f"{u['nickname']} ({u['r_count']})" for u in combined_request_counts]
    sizes = [generate_size(u['r_count'], total_requests) for u in combined_request_counts]

    pyplot.clf()
    fig1, ax1 = pyplot.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig1.savefig('tmp.png')

    await ctx.send(file=File('tmp.png'))

    os.remove('tmp.png')


@bot.event
async def on_message_edit(before, after):
    old_url = before.embeds[0].url
    url = after.embeds[0].url

    was_updated = not old_url and url and 'themoviedb.org/movie' in url
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
    await MovieRequestRepository.create(form)

    # FIXME - will send a message when this is the only server running
    # await after.channel.send(
    #     f"{new_embed.title} will be coming right up...")
