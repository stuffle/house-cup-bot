import discord
import time

from constants import *
from config import *


# user_id: {identity: "", set_by: user_id}
members = {}


class WhoisException(Exception):
    pass


async def whois_lookup(client, message):
    text = message.content
    args = text.split()
    msg = ""
    whois_example = "Examples: `~whois @stufflebear`, `whois stufflebear`, `whois 438450978690433024`"

    if message.channel.id in CSUA_PUBLIC_CHANNELS:
        raise WhoisException(
            "I won't reveal private CSUA information in public channels. "
            "Please ask me again in a private channel."
            )

    if len(args) != 2:
        raise WhoisException(
            "Please look people up one at a time, using "
            "the first word in their display name, their user ID, or "
            "their @mention.\n%s" % whois_example)

    person = args[1]
    user_id = 0
    mentions = message.mentions
    matched_names = 0

    # Given a mention
    if len(mentions) == 1:
        user_id = mentions[0].id
    # Given the user ID
    elif person.isdigit():
        user_id = int(person)
        # TODO: Edge case I'm too lazy to add: if someone's nickname is a digit
    else:
        # See if the argument matches the first word in someone's name
        members_of_guild = await message.guild.fetch_members().flatten()
        for m in members_of_guild:
            first_name = m.display_name.split(" ")[0]
            if first_name == person:
                user_id = m.id
                matched_names += 1
        if matched_names > 1:
            raise WhoisException(
                "More than one person has that name on display."
                " You'll have to look them up by either user ID or a mention.")

    if user_id not in members:
        if user_id == message.author.id:
            raise WhoisException(
                "I don't have an entry for you yet. "
                "Please set one with:\n`~identify @you whatever you want`")
        else:
            raise WhoisException(
                "I don't have an entry for them. "
                "But please do let me know when you find out who they are.")

    identity = members[user_id]["identity"]
    if user_id == message.author.id:
        msg = "You are: '%s'." % identity
    else:
        msg = "They are: '%s'." % identity
    
    return msg



def set_identity(client, message):
    msg = "Thank you for setting your identity."
    example_string = "Example: `~identify @you whatever you want`"

    args = message.content.split(" ")[1:]

    if len(message.mentions) > 1:
        raise WhoisException(
            "You can only set one person's identity at a time.")
    if len(message.mentions) == 0:
        raise WhoisException(
            "Please mention a user to log their identity. %s" % example_string)
    if len(args[0]) >= 1 and not args[0].startswith("<@"):
        # args[0] is defined because there is a mention in the message
        raise WhoisException(
            "Please put the mention as the first argument. %s" % example_string)

    setter = message.author
    member = message.mentions[0]
    new_identity = " ".join(args[1:])

    if new_identity == "":
        raise WhoisException(
            "Please provide an indentity. %s" % example_string)
    
    identity_already_exists = member.id in members
    if identity_already_exists:
        set_by = members[member.id]["set_by"]

        if set_by == member.id and setter.id != member.id:
            raise WhoisException(
            "You can not overwrite a self-defined identity.")

        previous_identity = members[member.id]["identity"]
        members[member.id]["set_by"] = setter.id
        members[member.id]["identity"] = new_identity
        msg = "You have successfully overwritten the old identity of '%s' with '%s'." % (previous_identity, new_identity)
    else:
        members[member.id] = {
            "set_by": setter.id,
            "identity": new_identity}
        msg = "You have successfully logged a new identity."
        if setter.id == member.id:
            msg = "%s No one but you can overwrite your own identity." % msg

    if member.id == STUFFLEBOT_ID:
        msg = ":pikachu_face: Is that all I am to you?"

    if message.channel.id in CSUA_PUBLIC_CHANNELS:
        msg = "%s I also want to warn you that this is a potentially public channel. If your identity is private, you may want to delete both your last message and this one." % msg

    return msg
