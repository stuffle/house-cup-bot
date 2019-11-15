import discord
from constants import *
from actions import *


# User ID to list of open proposals for that person
proposals = {}

# User IDs concatted together with dict of marriage info
# EG: "123|234" : {}
marriage_info = {}


class MarriageException(Exception):
    pass


newlywed_gifs = [
    ("https://cdn.discordapp.com/attachments/565884495023177728/629253632315097108/image0.gif",
        "The Simpsons: Homer is wearing a long-sleeved white wedding dress, holding a bouquet of pink flowers and wearing a crown woven of the same flowers. He lifts the skirt to step down the first step of the stairs in his home, exposing the garter he’s wearing over his knee, then he pauses, dropping the skirt and turning his head to breathe in the fragrance from the flowers."),
    ("https://cdn.discordapp.com/attachments/565884495023177728/629253929154117643/image0.gif",
        "The Simpsons: A young Homer and a young, pregnant Marge having a shotgun wedding in a dingy chapel. They look into each other’s eyes as the officiator is saying, “I now pronounce you man and wife.”"),
    ("https://cdn.discordapp.com/attachments/565884495023177728/629254122729766922/image0.gif",
        "The Simpsons: Homer standing under a wedding arch, presiding over the wedding of two men wearing matching suits and bow ties. Homer places his hand on his chest reverently as he says, “It brings me great joy to unite two such loving people.”"),
    ("https://cdn.discordapp.com/attachments/565884495023177728/629254275083796481/image0.gif",
        "The Simpsons: Homer standing under a wedding arch, presiding over the wedding of his sister-in-law Patty and her bride Veronica (who is secretly a man named Leslie). Homer is saying, “Queerly beloved, we’re here to join Veronica and Patty in matrimony.”"),
    ("https://cdn.discordapp.com/attachments/565884495023177728/629254479535013888/image0.gif",
        "The Simpsons: Homer standing under a wedding arch , presiding over the wedding of Cletus and Brandine, Springfield’s resident hillbillies. Homer is looking between the official document in his hands and the bride a groom with a confused expression on his face saying, “Wait an minute. Are you two brother and sister?”"),
    ("https://cdn.discordapp.com/attachments/565884495023177728/629254972697214997/image0.gif",
        "Homer is standing at the front door, angry at Mel Gibson who is at the threshhold. Homer reaches behind himself, grabbing Marge’s arm and then waving her wedding ring in Mel’s face saying, “You see this? It symbolizes that she’s my property, and I own her.” Marge doesn’t look too happy at this."),
    ("https://cdn.discordapp.com/attachments/565884495023177728/629255183796535296/image0.gif",
        "Homer wearing a suit and sitting at the front of one of Springfield Elementary’s classrooms. He’s holding a book, and his expression is looking a little vacant of intelligence as he says, ‘Well, Webster’s Dictionary defines a wedding as, “the process of removing weeds from one’s garden.”")
    ]


def marry(client, message):
    if len(message.mentions) == 0:
        raise MarriageException(
            "Mention a user to marry them.")
    if len(message.mentions) > 1:
        raise MarriageException(
            "Woah, slow down! Celebrate your marriages "
            "one at a time.")

    msg = ""
    embed = None

    proposer = message.author
    proposer_id = proposer.id
    partner = message.mentions[0]
    partner_id = partner.id
    times_married = 0
    marriage_id = "%d|%d" % (
        min(proposer_id, partner_id), max(proposer_id, partner_id))

    tenth_marriage = False

    # sigmabot auto accepts
    if partner_id == STUFFLEBOT_ID:
        # remarrying
        if marriage_id in marriage_info:
            times_married = marriage_info[marriage_id]["times_married"]
            marriage_info[marriage_id]["times_married"] = times_married + 1
            msg = "I'm very happy to remarry you! " \
                  "We are now married %d times." % (times_married + 1)
            if times_married + 1 == 10:
                tenth_marriage = True
        else:
            marriage_info[marriage_id] = {
                "times_married": 1
            }
            msg = "AHHHH!!!! I'm so happy that you want to marry me!!! :D\n\n"\
                  "*ahem*\n\nBy the authority vested in me, I now pronounce " \
                  "us bot and human! :tada:"

    # The Proposal is being accepted
    elif proposer_id in proposals and partner_id in proposals[proposer_id]:
        if marriage_id in marriage_info:
            times_married = marriage_info[marriage_id]["times_married"]
            marriage_info[marriage_id]["times_married"] = times_married + 1
            msg = "You renew your vows! You are now married %d times. " \
                  "Congratulations!! :tada:" % (times_married + 1)
            if times_married + 1 == 10:
                tenth_marriage = True
        else:
            # First marriage
            marriage_info[marriage_id] = {
                "times_married": 1
            }
            msg = "Congratulations to %s and %s—the newly weds!! " \
                  ":heart::heart::heart:" % (proposer.mention, partner.mention)
            embed = get_random_embed_same_quote(
                msg,
                newlywed_gifs,
                15761808)
        proposals[proposer_id].remove(partner_id)

    # This is a reproposal that hasn't been accepted yet
    elif partner_id in proposals and proposer_id in proposals[partner_id]:
        if marriage_id in marriage_info:
            msg = "%s is so eager to remarry %s that they will ask " \
                  "again and again." % (proposer.mention, partner.mention)
        else:
            msg = "%s gets down on one knee and stares pleadingly into " \
                  "the eyes of %s. \"Please, marry me,\" they beg." % (
                      proposer.mention, partner.mention)

    # Start proposal offer
    else:
        if partner_id in proposals:
            proposals[partner_id].append(proposer_id)
        else:
            proposals[partner_id] = [proposer_id]
        msg = "%s has proposed!!!\n\n" \
              "To accept this proposal, type '~marry %s'." % (
                  proposer.mention, proposer.mention)

    if tenth_marriage:
        tenth_gif_link = "https://cdn.discordapp.com/attachments/565884495023177728/629254720393052161/image0.gif"
        tenth_gif_caption = "The Simpsons: A young Homer and a young, pregnant Marge after their shotgun wedding. They are being handed their wedding certificate and the officiant is saying, “The tenth wedding is on the house.”"
        embed = get_random_embed_same_quote(
            msg,
            [(tenth_gif_link, tenth_gif_caption)],
            15761808)

    return (embed, msg)


def get_heart_string(client, times_married, emojis):
    if times_married < 0:
        return ":broken_heart:"
    elif times_married == 0:
        return emojis
    elif times_married > 1000:
        return ":sparkles:" + HEART_INFINITY + ":sparkles:"
    elif times_married == 777:
        return emojis + HEART_777
    elif times_married == 666:
        return emojis + HEART_666
    elif times_married >= 500:
        return get_heart_string(
            client, times_married - 500, emojis + RAINBOW_HEART_500)
    elif times_married == 420:
        return emojis + HEART_420
    elif times_married >= 100:
        return get_heart_string(
            client, times_married - 100, emojis + RAINBOW_HEART_100)
    elif times_married == 69:
        return emojis + HEART_69
    elif times_married >= 50:
        return get_heart_string(
            client, times_married - 50, emojis + RAINBOW_HEART_50)
    elif times_married >= 10:
        return get_heart_string(
            client, times_married - 10, emojis + RAINBOW_HEART_10)
    elif times_married >= 5:
        return get_heart_string(
            client, times_married - 5, emojis + RAINBOW_HEART_5)
    else:
        return get_heart_string(
            client, times_married - 1, emojis + ":hearts:")


async def see_marriages(client, message):

    text = message.content
    args = text.split()
    mentions = message.mentions

    user = message.author
    user_id = user.id

    if len(mentions) == 1:
        user = mentions[0]
        user_id = mentions[0].id
    elif len(args) > 1:
        raise MarriageException(
            "To look up another user's partners, mention them.")

    marriages = []
    msg_header = ":sparkles:__**%s's Partners**__:sparkles:\n" % user.mention

    for marriage_id in marriage_info.keys():
        if str(user_id) in marriage_id:
            marriages.append(marriage_id)

    count = 1
    marriage_msgs = []
    for marriage_id in marriages:
        people = marriage_id.split("|")
        people.remove(str(user_id))
        partner_id = int(people[0])
        partner = client.get_user(partner_id)

        times_married = marriage_info[marriage_id]["times_married"]
        if times_married != 0 and partner:
            emojis = get_heart_string(client, times_married, "")
            syntax = "`"
            if times_married < 0:
                syntax = "~~"
            partner_name = partner.name
            msg_line = "**%d** %s%s%s %s\n" % (
                count, syntax, partner_name, syntax, emojis)

            marriage_msgs.append(msg_line)
            count += 1

    # Form as many messages as it takes to send all of the marriages
    msgs = [msg_header]
    current_index = 0
    for msg in marriage_msgs:
        combined = msgs[current_index] + msg
        if len(combined) < 2000:
            msgs[current_index] = combined
        else:
            msgs.append(msg)
            current_index += 1
    return msgs


def divorce(client, message):
    if len(message.mentions) == 0:
        raise MarriageException(
            "Mention a user to divorce them.")
    if len(message.mentions) > 1:
        raise MarriageException(
            "Woah, slow down! Celebrate your divorces "
            "one at a time.")
    msg = ""
    divorcer = message.author
    divorcer_id = divorcer.id
    partner = message.mentions[0]
    partner_id = partner.id
    times_married = 0
    marriage_id = "%d|%d" % (
        min(divorcer_id, partner_id), max(divorcer_id, partner_id))

    if marriage_id in marriage_info:
        times_married = marriage_info[marriage_id]["times_married"]
        marriage_info[marriage_id]["times_married"] = times_married - 1
        marriage_info[marriage_id]["divorced"] = True
        if partner_id == STUFFLEBOT_ID:
            msg = "Oh. I...uh...okay. :sob:\nSorry, I just..." \
                  "I never expected this. "\
                  "I always thought we would be happy together. " \
                  "I don't know what I did wrong, but whatever it is, " \
                  "I'm sorry. I'm so sorry. I never wanted to hurt you. " \
                  "I love you. In fact, I think I'll always love you."
        else:
            msg = "You two have divorced. " \
                  "You are now married %d times." % (times_married - 1)
    else:
        msg = "You weren’t married before, but now you’re super not married."

    return msg


def bless(client, message):
    if message.author.id != STUFFLE_ID:
        raise MarriageException(
            "Sorry, but only stuffle can bless marriages.")

    p1 = 0
    p2 = 0
    if len(message.mentions) >= 2:
        p1 = message.mentions[0].id
        p2 = message.mentions[1].id
    elif len(message.mentions) == 1:
        p1 = message.mentions[0].id
        p2 = message.mentions[0].id
    else:
        raise MarriageException(
            "Mention two users to bless their marriage.")

    args = message.content.split(" ")[1:]
    if len(args) < 3 or not args[2].isdigit():
        raise MarriageException(
            "Proper syntax is `~bless @person @other_person 69`")
    blessed_amount = int(args[2])

    marriage_id = "%d|%d" % (
        min(p1, p2), max(p1, p2))

    if marriage_id not in marriage_info:
        raise MarriageException(
            "Marriages must exist before being blessed.")
    previous_marriages = marriage_info[marriage_id]["times_married"]
    marriage_info[marriage_id]["times_married"] = blessed_amount
    marriage_info[marriage_id]["blessed"] = blessed_amount - previous_marriages

    return "%s has blessed this marriage. %s" % (
        message.author.mention, get_heart_string(client, blessed_amount, ""))
