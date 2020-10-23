import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'what is your favorite movie leo?':
        response = 'let my puppets come is pretty good'
        await message.channel.send(response)


client.run(os.environ['DISCORD_TOKEN'])
