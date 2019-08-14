import discord
import time

from constants import *


# UserId: [{pact: string, holder: userID, timestamp: timestamp}]
pacts = {}


class PactException(Exception):
    pass


def form_pact(client, message):
    msg = "I have witnessed this pact and sealed it with blood " \
          "in my database. So mote it be."

    args = message.content.split(" ")[1:]
    if len(args) <= 1:
        raise PactException(
            "Please include both your pact and the person "
            "you're making it to. "
            "Example: `~pact I swear to @redhorse that I will "
            "write 5k words of my original this month.`")
    pact = " ".join(args)

    if len(message.mentions) > 1:
        raise PactException(
            "You can only form a pact with one person at a time.")
    if len(message.mentions) == 0:
        raise PactException(
            "Please mention a user to form your pact.")

    promiser = message.author
    holder = message.mentions[0]
    if holder.id == STUFFLEBOT_ID:
        raise PactException(
            "I'm sorry, but I only witness pacts.")

    if promiser.id in pacts:
        pacts[promiser.id].append({
            "pact": pact,
            "holder": holder.id,
            "timestamp": time.time()
        })
    else:
        pacts[promiser.id] = [{
            "pact": pact,
            "holder": holder.id,
            "timestamp": time.time()
        }]

    return msg


def release_pact(client, message):
    if len(message.mentions) != 1:
        raise PactException(
            "Mention one user to release them from their pact.")

    releaser = message.author
    promiser = message.mentions[0]

    if promiser.id not in pacts.keys():
        raise PactException("There are no pacts for %s" % promiser.mention)

    count = 1
    sworn_pacts = {}
    for pact in pacts[promiser.id]:
        if pact["holder"] == releaser.id:
            sworn_pacts[count] = pact
        count += 1

    if len(sworn_pacts.keys()) == 0:
        raise PactException(
            "%s has not sworn any pacts to you." % promiser.mention)

    pact_id = list(sworn_pacts.keys())[0]
    if len(sworn_pacts.keys()) > 1:
        args = message.content.split(" ")[1:]
        if len(args) < 2 or not args[1].isdigit():
            raise PactException(
                "%s has sworn multiple packs to you. Include the "
                "number of the pact you wish to relsease them from. "
                "You can get this number by viewing their pacts using "
                "`~pacts %s`. Then use this commands again with that number: "
                "`~release %s %d`" % (
                    promiser.mention, promiser.mention, promiser.mention,
                    pact_id))
        pact_id = int(args[1])
        if pact_id not in sworn_pacts.keys():
            raise PactException(
                "%d is not a pact ID you can release %s from." % (
                    pact_id, promiser.mention))

    finished_pact = sworn_pacts[pact_id]
    pacts[promiser.id].remove(pact)

    return "%s has released %s from their vow:\n\"%s\"" % (
        releaser.mention, promiser.mention, finished_pact["pact"])


def see_pacts(client, message):
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
            "To look up another user's pacts, mention them.")

    msg = ":page_with_curl: __**%s's Pacts**__ :page_with_curl:\n" % user.mention

    if user_id in pacts.keys():
        count = 1
        for pact in pacts[user_id]:
            msg += "**%d** %s\n" % (count, pact["pact"])
            count += 1

    return msg
