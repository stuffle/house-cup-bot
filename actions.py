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
    person_mention = default
    str_mentions = [m.mention for m in mentions]
    text_people = text.split(" ")[1:]

    if len(text_people) > len(mentions):
        stripped = [
            ''.join(c for c in x if c not in [".", ","]) for x in text_people]
        person_mention = ", ".join(stripped)
    elif len(mentions) > 0:
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
            "Disney’s Aladdin-Genie hugging Aladdin and Jasmine when they run up to each other, then pulling in Abu, Aladdin’s monkey-in-crime, then the Sultan and Raja, who are Jasmine’s father and pet tiger respectively, and then the magic carpet, before squeezing and cuddling them all tightly."),
        ("https://media.discordapp.net/attachments/553382529521025037/588586381786480640/hug-Hy4hxRKtW.gif",
            "Korra, from Avatar, picks up the air bending family in a hug, then is nuzzled by a giant dog."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594623420596224021/image0.gif",
            "The family from The Incredibles smile while they all embrace.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 15761808)


def hug(hugger, mentions, text):
    text_people = text.split(" ")[1:]
    args = " ".join(text_people).lower()
    everyone = ["everyone", "all", "y'all", "yall", "friends"]
    if len(mentions) > 1 or len(text_people) > 1 or args in everyone:
        return group_hug(hugger, mentions, text)
    victim = get_mention(mentions, text, "Friend")
    quote = "%s: you have been hugged by %s!" % (victim, hugger)
    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/592480821890514944/594587388219490331/f95e1e9bc953789b72d2a900cc00b9d75cd19fa3.gif",
            "A gray kitten with a white nose sinks onto its sibling, deepening their hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594476754140397568/image0.gif",
            "A monkey jumps into the waiting arms of its friend."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594475503302213632/image0.gif",
            "A human hand weaves its hand between a cat’s arms to rub its belly. The cat tightens its arms, drawing the human arm towards itself."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594475025575444490/image0.gif",
            "A guy embraces a lion, scratching its chin and resting his head on its."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594474506240655380/image0.gif",
            "A dog puts its arm around another dog. They shift onto their hind legs to fully embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594474143848595456/image0.gif",
            "The rabbit from Zootopia peppily hugs the Fox, who sighs."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594472225428602882/image0.gif",
            "Two primates walk towards each other, then embrace in a deep hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594471466792255489/image0.gif",
            "A cat embraces a dog three times its size, standing so that they can rub their cheeks together. The dog's tail wags quickly."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594470674786025482/image0.gif",
            "Two dogs sit next to each other. The one on the left puts its arms around the other, patting its chest."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594469134193131521/image0.gif",
            "Two cats cuddle on a bed. The little spoon cat gets up and climbs atop the other, laying back down in an adorable embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594468549779521536/image0.gif",
            "Two dogs sit happily side by side when one suddenly grabs the other in a tight hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594468330811817985/image0.gif",
            "A chicken walks into the waiting arms of a toddler, who embraces it fully."),
        ("https://thumbs.gfycat.com/EachAridBellfrog-size_restricted.gif",
            "A duck with drawn-on stick figure arms hugs a dog, rubbing its hand nub through the fur. Then, with its “hand” still on the dog, they walk away together."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594466674216927232/image0.gif",
            "A baby polar bear smiles as it rubs its face against an adult polar bear’s while hugging."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594618248524333080/image0.gif",
            "A mother cat puts its arm around her baby."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594618535271989268/image0.gif",
            "A guy laying on the ground with a cow pets his neck and face, then wraps his arms around the cow’s neck."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594618874196918302/image0.gif",
            "Two baby pandas fall over while hugging."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594620317704519681/image0.gif",
            "A sleepy cat hugging a stuffed cat, opens its eyes as it pulls its stuffed cat closer."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594620598853042199/image0.gif",
            "A gorilla barrel rolls through a window into an attic to hug a pig with the caption “Emergency Hug”."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594620923433189376/image0.gif",
            "Sullivan from Monsters Inc pulls Boo into a tender embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594621805336199169/image0.gif",
            "A cartoon ghost with tiny arms hugs the air with the caption “ghost hug! You can’t feel it, but it’s there!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594622146802876426/image0.gif",
            "Two cartoon bears hug with the caption “sending a hug just for you”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594622886963052554/image0.gif",
            "An anthropomorphized pig leaps onto its computer monitor in an enthusiast hug with the caption “sending u a cyber hog!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594623799912169508/image0.gif",
            "A white kitten pulls the hand of a human into a close hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594624092016082997/image0.gif",
            "A primate surprises Jane Goodall with a hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594624311441096790/image0.gif",
            "Two monkeys on leashes hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594625341939515396/image0.gif",
            "Two cartoon seals jump together in a hug with hearts in the background."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594638442432823322/image0.gif",
            "Simba and Rafiki embrace, patting each other’s backs, on an overlook."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594638989139378236/image0.gif",
            "A woman hugs a horse’s neck while the horse brings its head around to rest on the woman’s back."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594639362659057822/image0.gif",
            "Two cartoon ponies spin while hugging, then stand with their front hoofs pressed together."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594639727265710092/image0.gif",
            "A cartoon owl hugs a little white bird who closes its eyes happily."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594639908304322610/image0.gif",
            "A little white bird runs into the waiting arms of a mouse."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594640220117401604/image0.gif",
            "Snoopy hugs a little yellow bird with flowers in the background."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594640514083586094/image0.gif",
            "A young cat slowly reaches up to hug the camera."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594640626583339018/image0.gif",
            "Pikachu and Piplup embrace with hearts in their eyes."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594641313069269002/image0.gif",
            "A shiba dog embraces its owner, its tail wagging happily."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594641518128791579/image0.gif",
            "A baby hugs two puppies in its lap."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594641783124918292/image0.gif",
            "One dinosaur reaches out to hug another dinosaur and a volcano erupts in the background, causing lava to engulf them."),
        ("https://media.discordapp.net/attachments/592467136845447197/594621293614333952/hug1.gif",
            "A big yellow bird reaches out to hug a red bird who is walking by. The red bird hides its face with its wing and hurries away."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594642723903111220/image0.gif",
            "A dolphin and its trainer embrace underwater while floating upwards.")
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
