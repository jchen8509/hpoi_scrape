import discord
import os
import re
from discord.ext import tasks
from dotenv import load_dotenv
from enum import Enum
from Hpoi_scraping import fetchCards, hpoiCard, STATUS

load_dotenv()
token = os.getenv("TOKEN")

channel_id = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# python3 example_bot.py to run bot
@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
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
        # channel = bot.get_channel(channel_id)
        # await channel.send('Start spying on Hpoi <:miku_omega:1146239251596460072>')
        pollSite.start()
    if ("hpoi eepy" == message.content.lower() or "hpoi eepy" in message.content.lower()):
        # channel = bot.get_channel(channel_id)
        # await channel.send('No longer spying on Hpoi <:cat_cry:1146240394724655235>')
        pollSite.stop()

@tasks.loop(seconds = 300) # repeat after every 300 seconds
async def pollSite():
    try:
        channel = bot.get_channel(channel_id)
        # TODO: Make async and await instead
        cards = await fetchCards()
        embeds = map(card_to_embed,cards)
    except Exception as e: 
        # await channel.send('Found new update but I cannot get them <:cat_cry:1146240394724655235>')
        print(e)
    else:
        for embed in embeds:
            await channel.send(embed = embed)
        return

class YOUR_OWN_G_DANG_COLOR_MAP(Enum):
    purple = 0x9B59B6
    blue = 0x6495ED
    green = 0x82E0AA
    gold = 0xFFBF00
    red = 0xC70039
    salmon = 0xF5B7B1

STATUS_TO_COLOR: dict[STATUS, YOUR_OWN_G_DANG_COLOR_MAP] = {
    STATUS.NEW_ANNOUNCEMENT: YOUR_OWN_G_DANG_COLOR_MAP.purple,
    STATUS.IMG_UPDATE: YOUR_OWN_G_DANG_COLOR_MAP.blue,
    STATUS.INFO_UPDATE: YOUR_OWN_G_DANG_COLOR_MAP.blue,
    STATUS.PO_OPENED: YOUR_OWN_G_DANG_COLOR_MAP.green,
    STATUS.RELEASE_DATE: YOUR_OWN_G_DANG_COLOR_MAP.gold,
    STATUS.DELAYED: YOUR_OWN_G_DANG_COLOR_MAP.red,
    STATUS.RE_RELEASE: YOUR_OWN_G_DANG_COLOR_MAP.salmon
}

def card_to_embed(card: hpoiCard):
   print(card.status)
   embed = discord.Embed(title = card.status.value, url = card.link, color = STATUS_TO_COLOR.get(card.status).value)
   embed.add_field(name = card.name, value = '',inline = False)
   embed.add_field(name = "Origin", value = re.sub(r"[\n\t\s]*", "", card.origin), inline = True)
   embed.add_field(name = "Character", value = re.sub(r"[\n\t\s]*", "", card.character), inline = True)
   embed.add_field(name = "Manufacturer", value = card.manufacturer, inline = True)
   embed.add_field(name = "Illustrator", value = re.sub(r"[\n\t\s]*", "", card.illustrator), inline = True)
   embed.add_field(name = "Release Date", value = card.release_date, inline = True)
   embed.add_field(name = "Price", value = card.price, inline = True)
   embed.add_field(name = "Material", value = re.sub(r"[\n\t\s]*", "", card.material), inline = True)
   embed.add_field(name = "Scale", value = card.scale, inline = True)
   embed.add_field(name = "Dimension", value = card.dimension, inline = True)
   embed.set_image(url = card.img_src)
   return embed

bot.run(token)
