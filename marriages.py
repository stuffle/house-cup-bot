import discord
from constants import *


# User ID to list of open proposals for that person
proposals = {}

# User IDs concatted together with dict of marriage info
# EG: "123|234" : {}
marriage_info = {}


class MarriageException(Exception):
    pass


def marry(client, message):
    if len(message.mentions) == 0:
        raise MarriageException(
            "Mention a user to marry them.")
    if len(message.mentions) > 1:
        raise MarriageException(
            "Woah, slow down! Celebrate your marriages "
            "one at a time.")
    msg = ""
    proposer = message.author
    proposer_id = proposer.id
    partner = message.mentions[0]
    partner_id = partner.id
    times_married = 0
    marriage_id = "%d|%d" % (
        min(proposer_id, partner_id), max(proposer_id, partner_id))

    # stufflebot auto accepts
    if partner_id == STUFFLEBOT_ID:
        # remarrying
        if marriage_id in marriage_info:
            times_married = marriage_info[marriage_id]["times_married"]
            marriage_info[marriage_id]["times_married"] = times_married + 1
            msg = "I'm very happy to remarry you! " \
                  "We are now married %d times." % (times_married + 1)
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
        else:
            # First marriage
            marriage_info[marriage_id] = {
                "times_married": 1
            }
            msg = "Congratulations to %s and %s—the newly weds!! " \
                  ":heart::heart::heart:" % (proposer.mention, partner.mention)
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
        msg = "%s has proposed to %s!!!\n\n" \
              "To accept this proposal, type '~marry %s'." % (
                  proposer.mention, partner.mention, proposer.mention)

    return msg


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
    msg = ":sparkles:__**%s's Partners**__:sparkles:\n" % user.mention

    for marriage_id in marriage_info.keys():
        if str(user_id) in marriage_id:
            marriages.append(marriage_id)

    count = 1
    for marriage_id in marriages:
        people = marriage_id.split("|")
        people.remove(str(user_id))
        partner_id = int(people[0])
        partner = client.get_user(partner_id)

        times_married = marriage_info[marriage_id]["times_married"]
        if times_married != 0:
            emojis = get_heart_string(client, times_married, "")
            syntax = "`"
            if times_married < 0 or not partner:
                syntax = "~~"
            partner_name = str(partner_id)
            if partner:
                partner_name = partner.name
            msg_line = "**%d** %s%s%s %s\n" % (
                count, syntax, partner_name, syntax, emojis)

            msg = msg + msg_line
            count += 1

    return msg


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
