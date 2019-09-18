import discord
import time

from constants import *


# UserId: [{pact: string, holder: userID, timestamp: timestamp}]
pacts = {}
finished_pacts = {}
failed_pacts = {}


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
    pact = pact.replace(holder.mention, holder.name)
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


def release_pact(client, message, fulfilled=False):
    if len(message.mentions) != 1:
        raise PactException(
            "Mention one user to release them from their pact.")

    releaser = message.author
    promiser = message.mentions[0]

    if promiser.id not in pacts.keys():
        raise PactException("There are no pacts for %s" % promiser.mention)

    # This works by relying on the consistent ordering of Python's dicts
    # Which yeah...it's quite hacky
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
    if fulfilled:
        if promiser.id in finished_pacts:
            finished_pacts[promiser.id].append(finished_pact)
        else:
            finished_pacts[promiser.id] = [finished_pact]
    else:
        if promiser.id in failed_pacts:
            failed_pacts[promiser.id].append(finished_pacts)
        else:
            failed_pacts[promiser.id] = [finished_pact]
    pacts[promiser.id].pop(pact_id - 1)

    msg = "%s has released %s from their uncompleted vow:\n\"%s\"" % (
        releaser.mention, promiser.mention, finished_pact["pact"])
    if fulfilled:
        msg = "%s has acknowledged %s's completion of their vow:\n\"%s\"" % (
        releaser.mention, promiser.mention, finished_pact["pact"])
    return msg


def see_pacts(client, message, type="open"):
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

    the_pacts = pacts
    msg = ":page_with_curl: __**%s's Pacts**__ :page_with_curl:\n" % user.mention

    if type == "completed":
        the_pacts = finished_pacts
        msg = ":sparkles: __**%s's Completed Pacts**__ :sparkles:\n" % user.mention
    if type == "failed":
        the_pacts = failed_pacts
        msg = "%s __**%s's Failed Pacts**__ %s\n" % (
            YOU_TRIED_EMOJI, user.mention, YOU_TRIED_EMOJI)

    if user_id in the_pacts.keys():
        count = 1
        for pact in the_pacts[user_id]:
            msg += "**%d** %s\n" % (count, pact["pact"])
            count += 1

    return msg
