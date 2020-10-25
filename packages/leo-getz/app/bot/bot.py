from asgiref.sync import sync_to_async
from discord.ext import commands
from discord.ext.commands import Context

from core.repositories.user_repository import UserRepository

bot = commands.Bot(command_prefix='!')


@bot.command(pass_sontext=True)
async def stats(ctx: Context):
    author = ctx.message.author

    author_id = str(author.id)

    user_details = {
        'discord_id': author_id,
        'discord_username': author.name,
    }

    user = await UserRepository.get_or_create(data=user_details)

    cnt = await sync_to_async(user.movierequests_created.count)()

    await ctx.message.channel.send(
        f"{author.display_name} has requested {str(cnt)} movies.")
