import discord
import os
import re
from discord.ext import tasks
from dotenv import load_dotenv
from Hpoi_scraping import fetchCards, hpoiCard

load_dotenv()
token = os.getenv("TOKEN")

channel_id = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
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
    # Requested by Mei
    if ("nero" == message.content.lower() or " nero" in message.content.lower()):
        await message.channel.send('Umu!')

    # Start/Stop fetching updates
    if ("hpoi trace on" == message.content.lower() or "hpoi trace on" in message.content.lower()):
        channel = bot.get_channel(channel_id)
        # await channel.send('Start spying on Hpoi <:miku_omega:1146239251596460072>')
        pollSite.start()
    if ("hpoi eepy" == message.content.lower() or "hpoi eepy" in message.content.lower()):
        channel = bot.get_channel(channel_id)
        await channel.send('No longer spying on Hpoi <:cat_cry:1146240394724655235>')
        pollSite.stop()

@tasks.loop(seconds = 300) # repeat after every 300 seconds
async def pollSite():
    channel = bot.get_channel(channel_id)
    cards = fetchCards()
    embeds = map(card_to_embed,cards)
    for embed in embeds:
        await channel.send(embed=embed)
    return

def card_to_embed(card: hpoiCard):
   embed = discord.Embed(title = card.status, url = card.link, color = 0x9B59B6)
   embed.add_field(name = card.name, value = '', inline = False)
   embed.add_field(name = "Origin", value = re.sub(r"[\n\t\s]*", "", card.origin), inline = False)
   embed.add_field(name = "Character", value = re.sub(r"[\n\t\s]*", "", card.character), inline = False)
   embed.add_field(name = "Manufacturer", value = re.sub(r"[\n\t\s]*", "", card.manufacturer), inline = False)
   embed.add_field(name = "Illustrator", value = re.sub(r"[\n\t\s]*", "", card.illustrator), inline = False)
   embed.add_field(name = "Release Date", value = card.release_date, inline = False)
   embed.add_field(name = "Price", value = card.price, inline = False)
   embed.add_field(name = "Material", value = re.sub(r"[\n\t\s]*", "", card.material), inline = False)
   embed.add_field(name = "Scale", value = card.scale, inline = False)
   embed.add_field(name = "Dimension", value = card.dimension, inline = False)
   embed.set_image(url = card.img_src)
   return embed

bot.run(token)