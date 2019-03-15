import discord
import random


def get_random_embed(quote_dict, author):
    secure_random = random.SystemRandom()
    quote, gif = random.sample(quote_dict.items(), 1)[0]

    embed = discord.Embed(description=quote)
    embed.set_author(name=author + ":")
    embed.set_image(url=gif)
    return embed


def dumbledore():
    """
    Written by CHRain
    """
    quotes = {
        " I’m afraid after I take points from you, the likely result will be death caused by angry housemates, but do not fret. After all, to the well-organized mind, death is but the next great adventure. Good Luck. 50 points from Gryffindor! " : " https://media.giphy.com/media/720g7C1jz13wI/giphy.gif ",
        " Do you feel pain? Pain from losing house points, yet again? Remember, the fact that you can feel pain like this is your greatest strength. 50 points from Gryffindor! " : " https://media.giphy.com/media/xqn7gb9F4tl2U/giphy.gif ",
        " 20 points from Gryffindor! Anguish. It’s an emotion all of us must face at one point in our lives, I’m afraid. As a man who has lived that life, I give you wisdom: we must try not to sink beneath our anguish, but battle on. " : " https://media.giphy.com/media/14q7kvYacWa2I0/giphy.gif ",
        " Your act of kindness warms my heart and soothes my soul. Thank you little one, for typing the dumbledore command. It's lucky it's dark. I haven't blushed so much since Madam Pomfrey told me she liked my new earmuffs. 10 points to Gryffindor. " : " https://media.giphy.com/media/AOrThUuuOoDCg/giphy.gif ",
        " 30 points to Gryffindor! Congratulations! Off you trot, I am sure your Gryffindor housemates are waiting to celebrate with you, and it would be a shame to deprive them of this excellent excuse to make a great deal of mess and noise. " : " https://media.giphy.com/media/OU1marLMNNtnO/giphy.gif "
    }

    return get_random_embed(quotes, "Dumbledore")
