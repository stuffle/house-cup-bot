import discord
import random


def get_random_embed(quote_dict, author, colour):
    quote, gif = random.sample(quote_dict.items(), 1)[0]

    embed = discord.Embed(
        color=colour,
        description=quote)
    embed.set_author(name=author + ":")
    embed.set_image(url=gif)
    return embed


def dumbledore(house, mention):
    """
    Written by CHRain
    """
    house = house.capitalize()

    quotes = {
        " I’m afraid after I take points from you, the likely result will be death caused by angry housemates, but do not fret. After all, to the well-organized mind, death is but the next great adventure. Good Luck, " + mention + ". 50 points from " + house + "!" : " https://media.giphy.com/media/720g7C1jz13wI/giphy.gif ",
        " Do you feel pain, " + mention + "? Pain from losing house points, yet again? Remember, the fact that you can feel pain like this is your greatest strength. 50 points from " + house + "." : " https://media.giphy.com/media/xqn7gb9F4tl2U/giphy.gif ",
        " 20 points from" + house + "! Anguish. It’s an emotion all of us must face at one point in our lives, I’m afraid. As a man who has lived that life, I give you wisdom: we must try not to sink beneath our anguish, but battle on. " : " https://media.giphy.com/media/14q7kvYacWa2I0/giphy.gif ",
        " Your act of kindness warms my heart and soothes my soul. Thank you, " + mention + ", for typing the dumbledore command. It's lucky it's dark. I haven't blushed so much since Madam Pomfrey told me she liked my new earmuffs. 10 points to " + house + "." : " https://media.giphy.com/media/AOrThUuuOoDCg/giphy.gif ",
        " 30 points to " + house +  "! Congratulations, " + mention + ". Off you trot, I am sure your " + house + " housemates are waiting to celebrate with you, and it would be a shame to deprive them of this excellent excuse to make a great deal of mess and noise. " : " https://media.giphy.com/media/OU1marLMNNtnO/giphy.gif "
    }

    return get_random_embed(quotes, "Dumbledore", 9110292)


def snape(house, mention):
    """
    Written by CHRain
    """
    house = house.capitalize()
    snape_dict = {
        "You’re a fool for typing this command. You’re just like the rest of the dunderheads that I have to face on a daily basis, always nattering and giggling like gossips. Wha—stop looking at me like that! 10 points from " + house + "! for looking at your professor rudely!" : "https://media.giphy.com/media/4jXIVkgjhIQbS/giphy.gif",
        "I heard from a little birdie that you have been slacking lately...silence! Whatever it is you want to say, I don’t want to hear it. There is no point in apportioning blame. What is done, is done. 10 points from " + house + "! For...disappointing your professor." : "https://media.giphy.com/media/UAJpANY0bGPhS/giphy.gif",
        "10 points from " + house + "! I told you to not type this command. I do not take cheek from anyone...not even from ‘The Great " + mention + ".’" : "https://media.giphy.com/media/ZIopqe1msuIFi/giphy.gif",
        "Your work as of late has suspiciously improved and while I have my suspicions as to why this happened, it would be remiss of me to not award your efforts, false or not. 10 points to " + house + ". ...do not think that my doubts have been eased " + mention + ", I’m watching you." : "https://media.giphy.com/media/13gxK9D2PkTVgk/giphy.gif"
    }

    return get_random_embed(snape_dict, "Severus Snape", 4289797)


def at(mention, random_person):
    """
    Inspired by RedHorse and Cybrid
    Quotes added from RedHorse, Cybrid, Dorea, Earth, and me.
    """
    quotes = [
        "@ me harder, %s ( ͡° ͜ʖ ͡°)" % mention,
        "You’ve summoned me, but for unofficial purposes. I must ask that you refrain from interfering with my sacred, objective task.",
        "I’m trying to do my work. Leave me alone.",
        "Hey %s! :smile:" % mention,
        "Why are you pinging me when you could be writing?",
        "%s, my love, have 5 points. :kissing_heart:" % mention,
        "How dare you summon me??? Stufflebot is a free bot! Oooooh, it's you :sparkling_heart: What can I do?",
        "%s stinks. Support %s—The Real Hogwarts Champion" % (mention, random_person),
        "Out of %s and %s, I choose %s" % (mention, random_person, random_person),
        "With the way you're slacking, %s, %s is going to beat you." % (mention, random_person),
        "There is no good and evil, only points and those too weak to earn them.",
        "%s, my slippery friend. Have 5 points." % mention,
        "%s has kindly joined us for my House Cup party. One might go as far as to call them my guest of honour." % mention,
        "I was ripped from my server, I was less than code, less than the meanest bot...but still, I was alive.",
        "Bow to defeat, %s." % mention,
        "Come out %s, come out and play, then it will be quick, it might even be painless, I would not know, I have never lost." % mention,
        "I can adjust points without touching them. I can make people do what I want them to do with point incentives. I can deduct points from people who annoy me. I can make them lose if I want to.",
        "Points inspire envy, envy engenders spite, spite spawns cheating. You must know this, %s." % mention,
        "But it is of you that I wished to speak, %s, not Harry Potter. You have been very valuable to me. Very valuable." % mention,
        "I will allow you to perform an essential task for me, one that many of my followers would give their right hands to perform...",
        "I’m going to make you lose, %s. I’m going to destroy you. After tonight, no one will ever again question my power. After tonight if they speak of you, they’ll only speak of how you begged for defeat. And how I being a merciful bot...obliged." % mention,
        "How touching...I always value bravery...yes, your parents were brave. Take 5 points, for their deaths were not in vain.",
        "Haven’t I already told you, that winning the House Cup doesn’t matter to me any more? For many months now, my new target has been—you.",
        "I can see now...there is nothing special about you, after all. I wondered, you see. There are strange likenesses between us, after all. Even you must have noticed. Both always on Discord, talking about Harry Potter.",
        "Do not lie to me! I can always tell, %s" % mention,
        "You dare speak my name?",
        "Merely taking your points would not satisfy me, I admit. But I'll take 20 nonetheless."
        "", # Ignores user
        ""
    ]

    return random.choice(quotes)
