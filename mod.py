import discord
import random
import datetime
import pytz


utc = pytz.UTC


voting = {}

COS_GUILD_ID = 426319059009798146

SERVER_ID_TO_CHANNEL = {
    # Red's Writing Hood: house-cup-bot
    497039992401428498: 553382529521025037,
    # Test: general
    539932855845781524: 539932855845781530,
    # COS: bot-spam
    COS_GUILD_ID: 426322538944266240
}


class HouseCupException(Exception):
    pass


def is_mod(user, channel):
    stuffle_id = 438450978690433024
    user_is_mod = user.permissions_in(channel).administrator
    role_names = [role.name.lower() for role in user.roles]
    mod_role = "mod" in role_names
    return user_is_mod or mod_role or user.id == stuffle_id


async def get_channel_and_message(client, channel_id, message_id):
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

    return channel, message


def mod_message(text, mention, channel_id):

    # Do not allow spoiler tags outside of spoilers
    if text.count("||") >= 2 and channel_id != 553216475708522506:
        return "Hey %s, in an effort to be an accessible server, we don't allow the usage of spoiler tags outside of #spoilers (they don't work with screen readers). Help us be a welcoming server to all by removing the spoiler tags from your message. You can also help by captioning your images." % mention

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

    channel, message = await get_channel_and_message(client, channel_id, message_id)

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

    channel, message = await get_channel_and_message(client, channel_id, message_id)

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
        if count > amount and not is_mod(user, channel):
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


async def pick_winner(text, client):
    args = text.split()[1:]
    proper_format = "Proper formatting for this function is `~pickwinner MESSADE_ID CHANNEL_ID`"
    if len(args) != 2:
        raise HouseCupException(proper_format)
    if not args[0].isdigit() or not args[1].isdigit():
        raise HouseCupException(proper_format)

    message_id = int(args[0])
    channel_id = int(args[1])

    channel, message = await get_channel_and_message(client, channel_id, message_id)

    unique_users = []
    reactions = message.reactions
    for reaction in reactions:
        users = await reaction.users().flatten()
        for user in users:
            if user not in unique_users:
                unique_users.append(user)

    if len(unique_users) == 0:
        return "No one reacted to that message, so there is no winner."

    winner = random.choice(unique_users).name
    return "The winner is %s!" % winner


async def unwelcome(client):
    print("Running unwelcome")
    msg = "Unwelcoming complete!!"
    now = datetime.datetime.now(datetime.timezone.utc)
    week_ago = now - datetime.timedelta(days=7)
    welcome_id = 445996352363823104  # real welcome id
    # welcome_id = 601824945613570089 # Test server welcome ID
    guild_id = 426319059009798146
    guild = client.get_guild(guild_id)
    if not guild:
        return "I'm not in that guild."
    welcome_role = guild.get_role(welcome_id)
    boot_msg = "Hi! Sorry to kick you out of the server, but you haven’t chosen a House role in the week we gave you :frowning: If you’d like to come back to the server, here’s an invite link: https://discord.gg/BQD87kS   Please don’t forget this time, and thank you!"

    for member in welcome_role.members:
        joined = utc.localize(member.joined_at)
        if joined and joined < week_ago:
            role_names = [role.name.lower() for role in member.roles]
            if "slytherin" in role_names or "hufflepuff" in role_names or "ravenclaw" in role_names or "gryffindor" in role_names:
                await member.remove_roles(welcome_role, reason="They have had this role for a week.")
            else:
                await member.send(boot_msg)
                await member.kick(reason="User failed to pick a house role.")
    return msg


async def delete_history(client, message):
    channel = message.channel
    if not is_mod(message.author, channel):
        raise HouseCupException("Only mods may run this command.")

    if len(message.mentions) != 1:
        raise HouseCupException(
            "Mention one user to delete their history.")
    member = message.mentions[0]
    mention = member.mention

    await channel.send(
        "Running delete history for %s. "
        "I'll let you know when it's complete. "
        "This could take a while." % mention)

    for channel in message.guild.text_channels:
        try:
            await channel.purge(
                limit=None,
                after=member.joined_at,
                check=lambda msg: msg.author.id == member.id)
        except Exception:
            print(Exception)
    print("Deleted history for %s" % member.name)
    msg = "Finished running delete history for %s." % mention
    return msg


async def clear_channels(client, message=None):
    print("Clearing channels")

    if message:
        channel = message.channel
        if not is_mod(message.author, channel):
            raise HouseCupException("Only mods may run this command.")
        await channel.send(
            "Running clearchannels. "
            "I'll let you know when it's complete. "
            "This could take a while.")

    channels_to_clear = [
        # COS, #tea-and-hugs
        (COS_GUILD_ID, 595247008340508683),
        # COS, snap-snap
        (COS_GUILD_ID, 595247137898627082),
        # COS, feel-good
        (COS_GUILD_ID, 595247070793826386),
        # COS, sanity-checking
        (COS_GUILD_ID, 603211515625209857),
        # Test, clear
        (539932855845781524, 601903313310711878)
    ]

    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)

    for guild_id, channel_id in channels_to_clear:
        channel = client.get_channel(channel_id)
        if channel:
            await channel.purge(
                limit=None,
                before=week_ago,
                check=lambda msg: not msg.pinned)
        else:
            print("Did not run for %d" % channel_id)

    return "Ran clear channels!"


async def clear_channel_now(client, message):

    channel = message.channel
    if not is_mod(message.author, channel):
        raise HouseCupException("Only mods may run this command.")
    await channel.send(
        "Deleting all messages in this channel that weren't pinned...")

    await channel.purge(
        limit=None,
        check=lambda msg: not msg.pinned)

    return "Deleted non-pinned messages in this channel!"


async def chide(text, client):
    args = text.split()[1:]
    proper_format = "Proper formatting for this function is `~chide MESSADE_ID CHANNEL_ID`"
    if len(args) != 2:
        raise HouseCupException(proper_format)
    if not args[0].isdigit() or not args[1].isdigit():
        raise HouseCupException(proper_format)

    message_id = int(args[0])
    channel_id = int(args[1])

    channel, message = await get_channel_and_message(
        client, channel_id, message_id)
    await channel.send(
        "Hey, %s, in an effort to make our server more "
        "accesible we ask people to caption their images. "
        "Just transcribe the text and/or describe what it is depicting."
        " Thanks!" % message.author.mention)

    return "%s has been chided in %s." % (message.author.name, channel.name)
