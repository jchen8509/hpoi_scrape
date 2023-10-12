import discord
import os
from discord.ext import tasks
from dotenv import load_dotenv
from enum import Enum
from hpoi_scraping import fetchCards, hpoiCard, STATUS
import html

load_dotenv()
token = os.getenv("TOKEN")

channel_id = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# python3 example_bot.py to run bot
@bot.event
async def on_ready():
    # channel = bot.get_channel(channel_id)
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
   embed = discord.Embed(title = card.status.value, url = card.link, description = html.unescape(card.name), color = STATUS_TO_COLOR.get(card.status).value)
   embed.add_field(name = "Origin", value = "".join(html.unescape(card.origin)).split(), inline = True)
   embed.add_field(name = "Character", value = "".join(html.unescape(card.character)).split(), inline = True)
   embed.add_field(name = "Manufacturer", value = "".join(html.unescape(card.manufacturer).split()), inline = True)
   embed.add_field(name = "Illustrator", value = "".join(html.unescape(card.illustrator)).split(), inline = True)
   embed.add_field(name = "Release Date", value = card.release_date, inline = True)
   embed.add_field(name = "Price", value = card.price, inline = True)
   embed.add_field(name = "Material", value = card.material, inline = True)
   embed.add_field(name = "Scale", value = card.scale, inline = True)
   embed.add_field(name = "Dimension", value = card.dimension, inline = True)
   embed.set_image(url = card.img_src)
   return embed

bot.run(token)
