import discord
import random
import asyncio
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from calendar import monthrange
import datetime

from humor_commands import *


def get_random_embed_same_quote(quote, gif_and_caption, colour):
    """
    gif_and_caption is a list of tuples
    """
    gif, caption = random.sample(gif_and_caption, 1)[0]

    embed = discord.Embed(
        color=colour,
        description=quote)
    embed.set_image(url=gif)
    embed.set_footer(text="Gif Caption: " + caption)
    return embed


def get_mention(mentions, text, default="Harry Potter"):
    person_mention = ""
    str_mentions = [m.mention for m in mentions]

    if len(mentions) == 0:
        if text and len(text.split(" ")) > 1:
            person_mention = " ".join(text.split(" ")[1:])
        else:
            person_mention = default
    elif len(mentions) == 1:
        person_mention = mentions[0].mention
    else:
        person_mention = ", ".join(str_mentions)
    return person_mention


def kidnap(kidnapper, mentions, text):
    """Inspiration and gif contributions from Dorea"""
    victim = get_mention(mentions, text, "Dorea")
    quote = "%s has kidnapped %s!!!" % (kidnapper, victim)
    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/539932855845781530/569529962034626610/weee_kidnap.gif",
            "Woman lets go of doorway as a man in a black mask pulls her away with the caption “Okay! Weeeeeeee!”"),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569548311523098654/cat_kidnap_gif.gif",
            "Two hands reach in from off screen and grab a calm, black cat. As it is pulled away, the cat is unruffled as it slides across a tile floor."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569548870271369244/orange_cat_kidnapped.gif",
            "A person pulls with all their might to remove an orange cat from a room, but the cat successfully holds onto the doorway."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569550008928698369/oh_no_kidnap.gif",
            "Two masked men grab a man who says, \"Oh no, I'm being kidnapped!\""),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569550813954048060/monster-kidnapping-girl.gif",
            "A woman is standing by a blue door with a small window when suddenly an arm breaks the window and drags her through.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 0)


def group_hug(hugger, mentions, text):
    """Inspiration and gif contributions from Caty Pi"""
    victim = get_mention(mentions, text, "Everyone")
    quote = "%s: you have been hugged by %s!" % (victim, hugger)
    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523732652359686/image0.gif",
            "My Litttle Pony-Pinky Pie impossibly reaching off screen and pulling Twilight Sparkle, Fluttershy, Apple Jack, Rainbow Dash and Rarity into a hug."),
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523907064233996/image0.gif",
            "1st shot-Five girls jump onto screen and hug (their teacher?)  2nd shot-Five girls hug a classmate  3rd shot-Two girls are hugged by five other students who all pile onto hug one by one"),
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523944469168168/image0.gif",
            "The Simpsons-Homer Simpson being hugged by lots of children, including Rod and Tod, all eight of Apu’s children, Ralph Wiggum, and others. Another child, Üter, jumps on top of pile, hugging Homer’s face and squishing the other children."),
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523959446765578/image0.gif",
            "Disney’s Aladdin-Genie hugging Aladdin and Jasmine when they run up to each other, then pulling in Abu, Aladdin’s monkey-in-crime, then the Sultan and Raja, who are Jasmine’s father and pet tiger respectively, and then the magic carpet, before squeezing and cuddling them all tightly.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 15761808)


def pillage(person):
    """Inspiration and gif contributions from Dorea"""
    quote = "%s is on a pillaging spree!!!" % person
    gif_to_caption = [
        ("https://medievalkarl.files.wordpress.com/2015/02/7vh0ndg.gif",
            "A couple stand, peacefully framed by a stone window with vines. They scream when suddenly, the vikings charge."),
        ("https://www.eclectech.co.uk/b3ta/vikingbunny.gif",
            "A rabbit viking pillages a lawn by eating the grass."),
        ("https://66.media.tumblr.com/3ad6158c2bae0cf726539d6974ed6d5a/tumblr_o8s37xqzTF1tdy0nco1_500.gif",
            "Vikings cheer in front of a flaming wreckage."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569555567685664775/viking_battlefield.gif",
            "Vikings fight on an open field."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569556428092866648/viking_woman_strikes.gif",
            "A viking woman strikes down a man in front of her ship.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 13632027)


def wrestle(hugger, mentions):
    """Inspiration from RedHorse and other beta readers"""
    participants = [hugger]
    if len(mentions) == 1:
        participants.append(mentions[0].mention)
    else:
        return "Please mention one user to wrestle them."

    winner = random.choice(participants)
    participants.remove(winner)
    loser = participants[0]
    fluids = [
        "mud",
        "jelly",
        "icing",
        "blood",
        "melted chocolate",
        "soap",
        "chili"
    ]
    fluid = random.choice(fluids)

    responses = [
        "%s slips while stepping into the rink, making an easy victory for %s." % (
            winner, loser),
        "As soon as the match begins, %s tackles %s. They fall to the ground landing in the %s. They struggle for control until %s manages to flip them over, pinning %s and winning the match." % (
            loser, winner, fluid, winner, loser),
        "They size each other up for several moments before %s steps forward, slipping in the %s. Mid fall they reach out, grabbing %s and managing to bring them down too. %s is dazed, and %s takes the win." % (
            winner, fluid, loser, loser, winner),
        "%s manages to grasp the legs of %s, lifting them overhead and throwing them into the %s. %s is dazed, and %s takes the win." % (
            winner, loser, fluid, loser, winner),
        "They flail feebly at each other as if fighting off invisible bees. %s is out of breath first, allowing %s to subdue them." % (
            loser, winner),
        "%s does an impressive throwdown, making %s drink a mouthful of %s. %s splutters feebily for a moment before they tap out, losing the match." % (
            winner, loser, fluid, loser),
        "The battle, if you want to call it that, is short-lived. %s always said they weren’t the outdoorsy type. It's an easy victory for %s." % (
            loser, winner),
        "After a tense staredown, %s uses bubble beam! The ref calls foul on %s for the illegal use of Pokémon moves. %s wins!" % (
            loser, loser, winner),
        "%s stubs a toe and falls into %s. The fight was over before it began. %s shakes their head not quite believing it as they are declared the winner so quickly." % (
            loser, winner, winner),
        "%s tries to use the killing curse. The ref, aghast that a death eater has snuck into the match, ends it quickly. The ref needn't have worried—%s has never been able to cast the curse successfully. Harry smirked from the side-lines, pointing at his scar. %s wins." % (
            loser, loser, winner),
        "%s distracts %s with NSFW Tomarry pictures and does a successful tackle. The pictures land into the %s and the crowd storm the rings, eager for a better look! %s is trampled into the %s. %s wins!" % (
            loser, winner, fluid, loser, fluid, winner),
        "%s and %s face each other across the %s. Neither wants to end up in the %s. %s offers %s a cup of tea, and suggest they settle their differences like reasonable people. %s agrees and, after a lengthy discussion, they come to a mutually beneficial arrangement. According to their agreement, %s wins!" % (
            winner, loser, fluid, fluid, winner, loser, loser, winner)
    ]

    commentary = random.choice(responses)
    return "%s and %s step into a large pool filled with %s. %s" % (
        winner, loser, fluid, commentary
    )
