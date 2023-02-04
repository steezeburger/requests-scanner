import discord
import discord.ext.commands as commands
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext.commands import Cog, command

from core.repositories.user_repository import UserRepository
from discord_bot.cogs import BaconCog, StatsCog
from movie_requests.repositories import MovieRequestRepository, PlexMovieRepository


class Misc(Cog):
    @command()
    async def ping(self, ctx):
        print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW hat the absolute fuck')
        await ctx.send("Pong !")

    @command()
    async def echo(self, ctx, text: str):
        await ctx.send(text)


@pytest_asyncio.fixture
async def bot():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix="!",
                     intents=intents)
    await b._async_setup_hook()  # set up the loop

    await b.add_cog(BaconCog(b))
    await b.add_cog(StatsCog(b, (UserRepository,
                                 MovieRequestRepository,
                                 PlexMovieRepository)))
    await b.add_cog(Misc())

    dpytest.configure(b)
    return b


@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("!ping")
    assert dpytest.verify().message().content("Pong !")


# @pytest.mark.asyncio
# async def test_request_movie(bot):
#     await dpytest.message("https://themoviedb.org/movie/603")
#     assert dpytest.verify().message().contains().content(
#         "It looks like you're requesting a movie.")

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_stats_me(bot, mocker):
    await dpytest.message("!statsme")
    assert dpytest.verify().message().content(
        "TestUser0_0_nick has requested 0 movies.\n0 have been fulfilled.")
