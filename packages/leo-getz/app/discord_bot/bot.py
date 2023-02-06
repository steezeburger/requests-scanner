import re

import discord as discord
from discord.ext import commands

from core.repositories.user_repository import UserRepository
from discord_bot.cogs import StatsCog, BaconCog
from discord_bot.helpers import get_random_affirm, get_radarr_request_from_tmdb_info
from movie_requests.repositories import MovieRequestRepository, PlexMovieRepository
from services.radarr import Radarr
from services.tmdb import TMDB

MOVIE_DB_URL = 'https://themoviedb.org/movie'

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
    match = re.search(r'themoviedb\.org\/movie\/(\d*)-?(.*)', message.content)

    if match:
        await handle_request_message(message)

    await bot.process_commands(message)


async def handle_request_message(message):
    user = await UserRepository.get_or_create_from_author_async(message.author)

    # get the tmdb_id from the url and check if a request already exists
    match = re.search(r'themoviedb\.org\/movie\/(\d*)-?(.*)', message.content)

    if not match:
        return

    tmdb_id = None
    tmdb_id = match.group(1)
    tmdb_id = int(tmdb_id)
    existing_request = await MovieRequestRepository.get_by_tmdb_id_async(tmdb_id)
    if existing_request and existing_request.fulfilled:
        await message.channel.send(f"This request has already been fulfilled.")
        return
    if existing_request:
        await message.channel.send(f"This movie has already been requested.\r\n"
                                   f"Reach out to the server administrator if you think there is an issue.")
        return

    # get movie info from TMDB, so we can create a request for radarr
    movie_info = TMDB.get_movie_by_id(tmdb_id)

    if movie_info.get('belongs_to_collection'):
        await message.channel.send(f"This movie belongs to a collection, and I don't know how to handle that yet.\r\n"
                                   f"Try requesting just the individual movie.")
        return

    radarr_request = get_radarr_request_from_tmdb_info(movie_info)
    print(radarr_request)

    # creates the movie in Radarr
    Radarr.create_movie(radarr_request)

    # creates the request locally
    await MovieRequestRepository.create_async({
        'movie_title': movie_info['title'],
        'movie_url': f"{MOVIE_DB_URL}/{movie_info['id']}",
        'tmdb_id': tmdb_id,
        'created_by': user,
    })
    await message.channel.send(get_random_affirm(movie_info['title']))
