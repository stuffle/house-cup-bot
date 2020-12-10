import discord
from constants import *


async def parse_for_lols(message):
    text = message.content.lower()

    if "yabish" in text or "ya bish" in text:
        await message.add_reaction("🇾")
        await message.add_reaction("🇦")
        await message.add_reaction("🅱")
        await message.add_reaction("🇮")
        await message.add_reaction("🇸")
        await message.add_reaction("🇭")
        await message.add_reaction("‼️")

    if "cat facts" in text:
    	msg = "Thank you, %s, for subscribing to Cat Facts!" % message.author.display_name
    	await message.channel.send(msg.format(message))