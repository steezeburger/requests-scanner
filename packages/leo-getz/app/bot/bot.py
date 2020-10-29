from asgiref.sync import sync_to_async
from discord.ext import commands
from discord.ext.commands import Context

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
