import re

import discord as discord
from core.repositories.user_repository import UserRepository
from discord.ext import commands
from discord_bot.cogs import StatsCog, BaconCog
from discord_bot.helpers import get_random_affirm
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
    """
    Check message for url from themoviedb.org and create a MovieRequest if necessary.
    """

    is_request = MOVIE_DB_URL in message.content
    has_embed = len(message.embeds) > 0

    if is_request and not has_embed:
        # NOTE - because has_embed checks for an embed, there is a possibility that the embed was not
        await message.channel.send("It looks like you're requesting a movie.\r\n"
                                   "I fucked up though, so can you please try that again?")
        return

    if is_request and has_embed:
        await handle_request_message(message)

    await bot.process_commands(message)


async def handle_request_message(message):
    user = await UserRepository.get_or_create_from_author_async(message.author)
    embed = message.embeds[0]
    title = embed.title
    url = embed.url

    # get the tmdb_id from the url and check if a request already exists
    tmdb_id = None
    match = re.search(r'themoviedb\.org\/movie\/(\d*)-?(.*)', url)
    if match:
        tmdb_id = match.group(1)
        existing_request = await MovieRequestRepository.get_by_tmdb_id_async(tmdb_id)
        if existing_request and existing_request.fulfilled:
            await message.channel.send(f"This request has already been fulfilled.")
            return
        if existing_request:
            await message.channel.send(f"This movie has already been requested.\r\n"
                                       f"Reach out to the server administrator if you think there is an issue.")
            return

    await MovieRequestRepository.create_async({
        'movie_title': title,
        'movie_url': url,
        'tmdb_id': tmdb_id,
        'created_by': user,
    })
    await message.channel.send(get_random_affirm(title))
