# This example requires the 'message_content' intent.
import discord
from discord.ext import commands, tasks

token = 'TODO'

intents = discord.Intents.all()
intents.message_content = True

bot = discord.Client(intents=intents)

# python3 example_bot.py to run bot
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('testing'):
        await message.channel.send('Miku')

# @tasks.loop(seconds = 10) # repeat after every 10 seconds
# async def myLoop():
    # work


    # myLoop.start()

bot.run(token)