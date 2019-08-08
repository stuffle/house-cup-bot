import discord


STUFFLEBOT_ID = 542048148776943657

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
    elif times_married >= 500:
        heart_emoji_500 = str(client.get_emoji(609054991734538242))
        return get_heart_string(
            client, times_married - 500, emojis + heart_emoji_500)
    elif times_married >= 100:
        heart_emoji_100 = str(client.get_emoji(609054831671508994))
        return get_heart_string(
            client, times_married - 100, emojis + heart_emoji_100)
    elif times_married >= 50:
        heart_emoji_50 = str(client.get_emoji(609054469459804180))
        return get_heart_string(
            client, times_married - 50, emojis + heart_emoji_50)
    elif times_married >= 10:
        heart_emoji_10 = str(client.get_emoji(609049620814888990))
        return get_heart_string(
            client, times_married - 10, emojis + heart_emoji_10)
    elif times_married >= 5:
        heart_emoji_5 = str(client.get_emoji(609048811754618903))
        return get_heart_string(
            client, times_married - 5, emojis + heart_emoji_5)
    else:
        rainbow_heart = str(client.get_emoji(609071343434203186))
        return get_heart_string(
            client, times_married - 1, emojis + rainbow_heart)


def test_em(client, text):
    args = text.split()
    times_married = int(args[1])
    emojis = ""
    if times_married == 69:
        emojis = str(client.get_emoji(609056473355386880))
    elif times_married == 420:
        emojis = str(client.get_emoji(609065627025539085))
    else:
        emojis = get_heart_string(client, times_married, "")
    return emojis


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
        emojis = ""
        if times_married == 69:
            emojis = str(client.get_emoji(609056473355386880))
        elif times_married == 420:
            emojis = str(client.get_emoji(609065627025539085))
        else:
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
