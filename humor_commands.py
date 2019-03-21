import discord
import random


def get_random_embed(quote_dict, author, colour):
    secure_random = random.SystemRandom()
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
        "I heard from a little birdie that you have been slacking lately. . . silence! Whatever it is you want to say, I don’t want to hear it. There is no point in apportioning blame. What is done, is done. 10 points from " + house + "! For...disappointing your professor." : "https://media.giphy.com/media/UAJpANY0bGPhS/giphy.gif",
        "10 points from " + house + "! I told you to not type this command. I do not take cheek from anyone . . . not even from ‘the great " + mention + ".’" : "https://media.giphy.com/media/ZIopqe1msuIFi/giphy.gif",
        "Your work as of late has suspiciously improved and while I have my suspicions as to why this happened, it would be remiss of me to not award your efforts, false or not. 10 points to " + house + ". ...do not think that my doubts have been eased " + mention + ", I’m watching you." : "https://media.giphy.com/media/13gxK9D2PkTVgk/giphy.gif"
    }

    return get_random_embed(snape_dict, "Severus Snape", 4289797)
