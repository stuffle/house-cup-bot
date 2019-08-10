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
            msg = "%s is in so eager to remarry %s that they will ask " \
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
    if times_married <= 0:
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


def test_em(client, text):
    args = text.split()
    times_married = int(args[1])
    return get_heart_string(client, times_married, "")


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
        emojis = get_heart_string(client, times_married, "")
        msg_line = "**%d** `%s` %s\n" % (
            count, partner.name, emojis)

        msg = msg + msg_line
        count += 1

    return msg


def divorce(client, message):
    msg = "RIP"

    # Normal divorce

    # Extra divorce

    return msg
