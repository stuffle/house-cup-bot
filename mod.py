import discord
import random
import datetime
import pytz
import mimetypes

from constants import *


utc = pytz.UTC

# Record of all the posts that are being monitored for voting
voting = {}

# Users that should have the #mod-pings role added to them when they join COS
imprisoned = {}


CAPTIONS_NOT_REQUIRED = [
    SNAP_SNAP, SHITPOSTING, NSFW_SHITPOSTING,
    ART_CHANNEL, ART_DISCUSSION, NSFW_ART, NSFW_ART_DISCUSSION,
    CHALLENGE_TIME,
    SFW_FLUFF, GAMING,
    IMAGES_TEST]


class HouseCupException(Exception):
    pass


def is_mod(user, channel):
    user_is_mod = user.permissions_in(channel).administrator
    role_names = [role.name.lower() for role in user.roles]
    mod_role = "mod" in role_names
    return user_is_mod or mod_role or user.id == STUFFLE_ID


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


async def mod_message(client, message):
    text = message.content.lower()
    mention = message.author.mention
    channel_id = message.channel.id
    guild_id = message.guild.id
    msg = ""

    # Do not mod messages from bots
    if message.author.bot:
        return msg

    # Do not allow spoiler tags outside of spoilers
    spoilers_allowed = [
        SPOILERS_CHANNEL_ID, SANITY_CHECKING, MOD_MINUTES, SHOP_TALK,  # COS
        MOD_CHAT,  # Writing
        TODO]  #Test
    if text.count("||") >= 2 and channel_id not in spoilers_allowed:
        msg = "Hey %s, in an effort to support **our members who are blind or use screen readers** for other reasons, **we don't allow the usage of spoiler tags** outside of #spoilers (they don't work with screen readers). Help us be a welcoming server to all by removing the spoiler tags from your message. You can also help by captioning your images." % mention

    # Mod messages that contain images for No Imaj role users in COS
    if (guild_id == COS_GUILD_ID or guild_id == TEST_GUILD_ID):
        if channel_id not in CAPTIONS_NOT_REQUIRED:
            role_names = [role.name for role in message.author.roles]
            if "No Imaj" in role_names and len(message.attachments) >= 1:
                for attachment in message.attachments:
                    file_type, encoding = mimetypes.guess_type(attachment.filename)
                    if file_type and "image" in file_type:
                        contains_identifier = "id" in text or "caption" in text or "alt text" in text or "image" in text
                        if not contains_identifier or len(text.split(" ")) < 10:
                            msg = (
                                "Hey %s, since you have the No Imaj role, "
                                "we require you to post image IDs with your image. "
                                "Your image ID must contain at least 10 words "
                                " and be formatted like '[Image ID: description]'. "
                                "I've deleted your message because it did not meet "
                                "this requirement. You may repost if you follow these guidlines." % mention)
                            print("Deleteing a message from %s with file: %s and text:%s" % (
                                message.author.name, attachment.filename, text))
                            await message.delete()
                            return msg

    return msg


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


async def on_join(client, member):
    if member.guild.id == COS_GUILD_ID:
        if member.id in imprisoned:
            mod_pings_role = member.guild.get_role(602956352565805087)
            await member.add_roles(
                mod_pings_role, reason="User ID is in the imprisoned list.")
            reason = imprisoned[member.id]
            print("The prisoner has come! %d:%s" % (member.id, reason))
            channel = client.get_channel(SANITY_CHECKING)
            await channel.send(
                "%s has rejoined the server."
                " I have locked them in #mod-pings."
                "They were `~imprison`ed for:\n\"%s\"" % (member.name, reason))
        else:
            welcome_role = member.guild.get_role(445996352363823104)
            await member.add_roles(welcome_role)


async def on_guild_member_update(client, before, after):
    if after.guild.id not in [COS_GUILD_ID, TEST_GUILD_ID]:
        return

    mod_pings_role = after.guild.get_role(602956352565805087)
    if mod_pings_role in after.roles and mod_pings_role not in before.roles:
        channel = client.get_channel(SANITY_CHECKING)
        await channel.send("%s is now in #mod-pings." % after.name)


def imprison(client, message):
    if not is_mod(message.author, message.channel):
        raise HouseCupException(
            "Only mods can imprison people.")
    if message.guild.id != COS_GUILD_ID:
        raise HouseCupException(
            "This command currently only works in COS.")
    args = message.content.split(" ")[1:]
    if len(args) < 2 or not args[0].isdigit():
        raise HouseCupException(
            "Proper formatting is `~imprison USER_ID reason`")
    user_id = int(args[0])
    guild = client.get_guild(COS_GUILD_ID)
    member = guild.get_member(user_id)
    in_server = ""
    if member:
        in_server = " Heads up that they are currently in the " \
                    "server with the name: %s" % member.name
    reason = " ".join(args[1:])
    imprisoned[user_id] = reason
    return "I will imprison them if they join the COS again.%s" % in_server


def view_imprisoned(client, message):
    if not is_mod(message.author, message.channel):
        raise HouseCupException(
            "Only mods can view the imprisoned people.")
    msg = "**__Locked in Mod-Pings on Rejoin__**\n"
    count = 1
    for user_id in imprisoned:
        msg += "**%d** `%d`: %s\n" % (count, user_id, imprisoned[user_id])
        count += 1
    return msg


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
    boot_msg = "Hi! Sorry to kick you out of the server, but you haven’t chosen a House role in the week we gave you :frowning: If you’d like to come back to the server, here’s an invite link: https://discord.gg/H8NJek9   Please don’t forget this time, and thank you!"

    for member in welcome_role.members:
        joined = utc.localize(member.joined_at)
        if joined and joined < week_ago:
            role_names = [role.name.lower() for role in member.roles]
            if "slytherin" in role_names or "hufflepuff" in role_names or "ravenclaw" in role_names or "gryffindor" in role_names or "mod pings" in role_names or "time out" in role_names:
                await member.remove_roles(welcome_role, reason="They have had this role for a week.")
            else:
                try:
                    print("Booting %s from the server as part of unwelcome" % member.name)
                    await member.send(boot_msg)
                    await member.kick(reason="User failed to pick a house role.")
                except Exception as ex:
                    msg = "Error on %s" % member.name
    return msg


async def delete_history(client, message, all_history=True):
    topic_keyword = "~deletesomehistory exempt"

    channel = message.channel
    if not is_mod(message.author, channel):
        raise HouseCupException("Only mods may run this command.")

    if len(message.mentions) != 1:
        raise HouseCupException(
            "Mention one user to delete their history.")
    member = message.mentions[0]
    mention = member.mention
    print("Running deletehistory for %s" % mention)

    command_str = "all"
    if not all_history:
        command_str = "some"
    explanation_str = "This will delete *every* message by %s." % mention
    if not all_history:
        explanation_str = "This will delete every message by %s, except messages that are pinned or in channels with `%s` in the topic." % (
            mention, topic_keyword)

    await channel.send(
        "Running delete %s history for %s. %s\n"
        "I'll let you know when it's complete. "
        "This could take a while." % (
            command_str, mention, explanation_str))

    for channel in message.guild.text_channels:
        save_in_delete_some = channel.topic and (topic_keyword in channel.topic)
        if all_history or not save_in_delete_some:
            try:
                delete_check = lambda msg: msg.author.id == member.id
                if not all_history:
                    delete_check = lambda msg: msg.author.id == member.id and not msg.pinned
                await channel.purge(
                    limit=None,
                    check=delete_check)
            except Exception as ex:
                print("Unable to purge %s." % channel.name)
                print(str(ex))
    print("Deleted history for %s" % member.name)
    msg = "Finished running delete history for %s." % mention
    return msg


async def clear_channels(client, message=None):

    if message:
        channel = message.channel
        if not is_mod(message.author, channel):
            raise HouseCupException("Only mods may run this command.")
        await channel.send(
            "Running clearchannels. "
            "I'll let you know when it's complete. "
            "This could take a while.")

    channels_to_clear = [
        (COS_GUILD_ID, TEA_AND_HUGS),
        (COS_GUILD_ID, SNAP_SNAP),
        (COS_GUILD_ID, FEEL_GOOD),
        (COS_GUILD_ID, SANITY_CHECKING),
        (COS_GUILD_ID, MOD_PINGS),
        (COS_GUILD_ID, HALL_MONITORS),
        (COS_GUILD_ID, NSFW)
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


async def tell(client, message, function_name, rebuke):
    role_names = [role.name.lower() for role in message.author.roles]
    hall_monitor_role = "here to help" in role_names
    if not(is_mod(message.author, message.channel) or hall_monitor_role):
        raise HouseCupException(
            "Only mods and hall monitors may use this command")

    text = message.content.lower()
    args = text.split()[1:]
    proper_format = "Proper formatting for this function is " \
                    "`~%s MESSADE_ID CHANNEL_ID`" % function_name
    if len(args) != 2:
        raise HouseCupException(proper_format)
    if not args[0].isdigit() or not args[1].isdigit():
        raise HouseCupException(proper_format)

    message_id = int(args[0])
    channel_id = int(args[1])

    if function_name in ["caption", "captionshame"]:
        if channel_id in CAPTIONS_NOT_REQUIRED:
            return "That channel does not require captions."

    channel, message = await get_channel_and_message(
        client, channel_id, message_id)
    await channel.send(rebuke % message.author.mention)

    return "%s has been chided in #%s." % (
        message.author.name, channel.name)


async def caption(message, client):
    rebuke = (
        "Hey, %s, in an effort to make our server more "
        "**accessible to blind people and others that use screen readers**"
        " we ask people to caption their images. "
        "Just transcribe the text and/or describe what it is depicting."
        " Thanks!")
    return await tell(client, message, "caption", rebuke)


async def captionshame(message, client):
    rebuke = (
        "Hey, %s, by not captioning your image, you’re "
        "**excluding blind people and others who use screen readers**."
        " The world is ableist enough. Do better.")
    return await tell(client, message, "captionshame", rebuke)
