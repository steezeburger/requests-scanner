import discord as discord
from core.repositories.user_repository import UserRepository
from discord.ext import commands
from discord_bot.cogs import StatsCog, BaconCog
from movie_requests.repositories import MovieRequestRepository, PlexMovieRepository

MOVIE_DB_URL = 'themoviedb.org/movie'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(BaconCog(bot))

    await bot.add_cog(StatsCog(bot, (UserRepository,
                                     MovieRequestRepository,
                                     PlexMovieRepository)))
    print(f'Connected to Discord!')


@bot.event
async def on_message(message):
    is_request = MOVIE_DB_URL in message.content
    has_embed = len(message.embeds) > 0

    if is_request and has_embed:
        user = await UserRepository.get_or_create_from_author_async(
            message.author)
        embed = message.embeds[0]
        form = {
            'movie_title': embed.title,
            'movie_url': embed.url,
            'created_by': user,
        }
        await MovieRequestRepository.create_async(form)

    await bot.process_commands(message)


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

    user = await UserRepository.get_or_create_from_author_async(author)
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
