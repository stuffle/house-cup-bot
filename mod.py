import discord


voting = {}

SERVER_ID_TO_CHANNEL = {
    # Red's Writing Hood: house-cup-bot
    497039992401428498: 553382529521025037,
    # Test: general
    539932855845781524: 539932855845781530,
    # COS: bot-spam
    426319059009798146: 426322538944266240
}


class HouseCupException(Exception):
    pass


def is_mod(user, channel):
    stuffle_id = 438450978690433024
    user_is_mod = user.permissions_in(channel).administrator
    role_names = [role.name.lower() for role in user.roles]
    mod_role = "mod" in role_names
    return user_is_mod or mod_role or user.id == stuffle_id


def mod_message(text, mention, channel_id):

    # Do not allow spoiler tags outside of spoilers
    if text.count("||") >= 2 and channel_id != "553216475708522506":
        return "Hey %s, we don't allow the usage of spoiler tags outside of #spoilers due to their inaccessibility with screen readers. Please remove them from your message. Thanks!" % mention

    return ""


async def check_reactions(payload, client):
    # Check reactions on messages that are being monitored for voting
    message_id = payload.message_id

    # Skip checking if we're not monitoring the message
    if message_id not in voting:
        return
    channel_id = voting[message_id]["channel_id"]
    if channel_id != payload.channel_id:
        return

    channel = client.get_channel(channel_id)
    try:
        message = await channel.fetch_message(message_id)
    except Exception:
        raise HouseCupException("Message %d could not be found." % message_id)

    # If user is a mod, react limits do not apply
    user_id = payload.user_id
    user = client.get_user(user_id)
    # if is_mod(user, channel):
    #    return

    amount = voting[message_id]["amount"]
    count = 0
    reactions = message.reactions
    for reaction in reactions:
        users = await reaction.users().flatten()
        if user in users:
            count += 1

    if count > amount:
        await message.remove_reaction(payload.emoji, user)
        msg = "%s: The message you just reacted to is a voting message " \
              "that only allows %d votes. " \
              "Your latest vote exceeds that limit, so I removed it." % (
                  user.mention, amount)
        send_channel_id = SERVER_ID_TO_CHANNEL[payload.guild_id]
        send_channel = client.get_channel(send_channel_id)
        await send_channel.send(msg)


async def monitor_voting(text, is_mod, client):
    if not is_mod:
        raise HouseCupException("Only mods can set up voting monitoring.")

    args = text.split()[1:]
    proper_format = "Proper formatting for this function is `~startmonitoring MESSADE_ID CHANNEL_ID AMOUNT`"
    if len(args) != 3:
        raise HouseCupException(proper_format)
    if not args[0].isdigit() or not args[1].isdigit() or not args[2].isdigit():
        raise HouseCupException(proper_format)

    message_id = int(args[0])
    channel_id = int(args[1])
    amount = int(args[2])

    channel = client.get_channel(channel_id)
    if not channel:
        raise HouseCupException(
            "I can't find that channel. Please try again.")

    message = None
    try:
        message = await channel.fetch_message(message_id)
    except Exception:
        raise HouseCupException("Invalid message ID. Please try again")
    if not message:
        raise HouseCupException(
            "I can't find that message. Please try again.")

    voting[message_id] = {
        "channel_id": channel_id,
        "amount": amount
    }

    # Check existing reactions
    user_to_count = {}
    reactions = message.reactions
    for reaction in reactions:
        users = await reaction.users().flatten()
        for user in users:
            if user in user_to_count:
                user_to_count[user] = user_to_count[user] + 1
            else:
                user_to_count[user] = 1
    for user in user_to_count:
        count = user_to_count[user]
        #  and not is_mod(user, channel)
        if count > amount:
            msg = "%s: You have reacted to the vote in %s with %d votes, " \
                  "but it only allows %d votes. Please remove your extra " \
                  "reaction(s)" % (user.mention, channel.name, count, amount)
            send_channel_id = SERVER_ID_TO_CHANNEL[channel.guild.id]
            send_channel = client.get_channel(send_channel_id)
            await send_channel.send(msg)

    return "I'll make sure no one reacts more than %d times to that " \
           "message. :eyes:" % amount


def stop_monitor_voting(text, is_mod):
    if not is_mod:
        raise HouseCupException("Only mods can remove voting monitoring.")

    args = text.split()[1:]
    if len(args) != 1 or not args[0].isdigit():
        raise HouseCupException(
            "Unrecognized argument(s). Correct formatting is `~stopmonitoring MESSAGE_ID`.")

    message_id = int(args[0])
    if message_id not in voting.keys():
        raise HouseCupException("I'm already not montioring that message!")

    del voting[message_id]
    return "I will no longer creep on that message."


def show_monitors(text, is_mod):
    if not is_mod:
        raise HouseCupException(
            "Sorry, but only mods can view all the monitors.")

    msg = ",".join([str(k) for k in voting.keys()])
    if msg:
        return "I am monitoring these messages: %s" % msg
    return "I'm not monitoring anything right now."
