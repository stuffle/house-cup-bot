import discord
from config import *


DOCS_LINK = "https://docs.google.com/document/d/1z03xR7jpi-oXwmI9N1XpU6N9" \
            "0BnXmj5ptyASdWnIkNA/edit?usp=sharing"
CAPTION_DOC_LINK = "https://docs.google.com/document/d/1VXoi-oesHpQ1l3payu" \
                   "NtEeQFfD_Dht3Emc3JIznOZXU/edit?usp=sharing"
COLOR = 6095788


def help_command(message, prefix):
    guild_id = message.guild.id
    text = message.content.lower()
    args = text.split()

    if len(args) == 1:
        return general_help(prefix, guild_id)

    arg = args[1]
    embed = None

    # Join and Leave
    if arg == "join":
        msg = "Join the House Cup with your current house role. \n" \
              "Unless you leave and rejoin, you will have your current" \
              " username for the entirety of the month." \
              "\n\nExample: `%sjoin`" % prefix
        embed = discord.Embed(
            title="Join Help",
            color=COLOR,
            description=msg)
    elif arg == "leave":
        msg = "Leave the House Cup. You will lose every point you've earned."\
              "\n\nExample: `%sleave`" % prefix
        embed = discord.Embed(
            title="Leave Help",
            color=COLOR,
            description=msg)
    elif arg == "time":
        msg = "See how much time remains until the end of the House Cup."\
              "\n\nExample: `%stime`" % prefix
        embed = discord.Embed(
            title="Time Help",
            color=COLOR,
            description=msg)

    # Logging Points
    elif arg == "daily":
        msg = "Log 5 points for doing any sort of creative fandom work. " \
              "It doesn't matter how little or how much you did. " \
              "Anything counts. :heart:\n\n" \
              "You must log your days work within 24 hours of doing it." \
              " Dailies can be logged once every eight hours, " \
              "but please do not log more than one a day." \
              "\n\nExample: `%sdaily`" % prefix
        embed = discord.Embed(
            title="Daily Help",
            color=COLOR,
            description=msg)
    elif arg == "post":
        msg = "Log 10 points each time you post something " \
              "other than art. For art, use `~art`." \
              " See the [FAQ](%s) in the house cup doc for " \
              "more info on what counts." \
              "\n\nExample: `%spost`" % (DOCS_LINK, prefix)
        embed = discord.Embed(
            title="Post Help",
            color=COLOR,
            description=msg)
    elif arg == "beta":
        msg = "Log 10 points each time you beta read a work, " \
              "or participate in a workshop as a reader." \
              "\n\nExample: `%sbeta`" % prefix
        embed = discord.Embed(
            title="Beta Help",
            color=COLOR,
            description=msg)
    elif arg == "art":
        msg = "Log 5, 10, 15, or 20 points for your art. " \
              "For visual art, full color earns 20 points, " \
              " flat color earns 15, line art earns 10, and a sketch earns 5. " \
              "See the [FAQ](%s) in the House Cup Documentation for more info." \
              "\n\nExample: `%sart 10`" % (DOCS_LINK, prefix)
        embed = discord.Embed(
            title="Art Help",
            color=COLOR,
            description=msg)
    elif arg == "workshop":
        msg = "Log 30 points when you contribute a work to the weekly " \
              "workshop. If you were a reviewer, use `%sbeta` to log " \
              "your points." \
              "\n\nExample: `%sworkshop`" % (prefix, prefix)
        embed = discord.Embed(
            title="Workshop Help",
            color=COLOR,
            description=msg)
    elif arg == "exercise":
        msg = "Log 5 workshop points when you either contribute a work to " \
              "the weekly exercise in the writing server or participate as a reader. " \
              "Do this command twice if you do both!" \
              "\n\nExample: `%sexercise`" % prefix
        embed = discord.Embed(
            title="Exercise Help",
            color=COLOR,
            description=msg)
    elif arg == "comment":
        msg = "Log 1 point for any comment and 5 points per essay-length " \
              "comment. " \
              "See the [FAQ](%s) in the house cup doc for " \
              "more info on which to use." \
              "\n\nExamples: `%scomment` for regular comments and `%scomment" \
              " extra` for essay-length comments." % (
                  DOCS_LINK, prefix, prefix)
        embed = discord.Embed(
            title="Comment Help",
            color=COLOR,
            description=msg)
    elif arg == "excred":
        msg = "Use `%sexcred AMOUNT`, where amount is a positive number.\n\n" \
              "Check the [document](%s) for this month's extra credit " \
              "challenge and its corresponding points. " \
              "Maximum Extra Credit is 50 points per month." \
              "\n\nExample: `%sexcred 10`" % (prefix, DOCS_LINK, prefix)
        embed = discord.Embed(
            title="Extra Credit Help",
            color=COLOR,
            description=msg)
    elif arg == "wc" or arg == "wordcount" or arg == "word_count":
        msg = "Log one point per 1000 words you've posted, rounded to the " \
              "nearest 1000.\n\n" \
              "Example: `%swc 9000` to log 9000 total words this month or"\
              " `%swc add 3000` to add 3000 words to your total." % (
                  prefix, prefix)
        embed = discord.Embed(
            title="Word Count Help",
            color=COLOR,
            description=msg)
    elif arg == "remove":
        msg = "Use `%sremove CATEGORY` to remove points from a given category"\
              ". CATEGORY may be `daily`, `post`, `beta`, `workshop`, " \
              "`comment`, or `excred`. If you are removing extra credit or art " \
              "points, you must provide the amount of points to remove. " \
              "If you want to remove points from your word count, use " \
              "`%swc TOTAL_WC` to reset your total word count." \
              "\n\nExamples: `%sremove daily`, `%sremove excred 10`, " \
              "%s`remove comment`, `%sremove comment extra`" % (
                  prefix, prefix, prefix, prefix, prefix, prefix)
        embed = discord.Embed(
            title="Remove Points Help",
            color=COLOR,
            description=msg)

    # Viewing Points
    elif arg == "points":
        msg = "Show how many of each kind of point you have. "\
              "You many mention a person to look up their points." \
              "\n\nExamples: `%spoints`, `%spoints @Earth`" % (prefix, prefix)
        embed = discord.Embed(
            title="Show Points Help",
            color=COLOR,
            description=msg)
    elif arg == "housepoints":
        msg = "Show your total house points and the points of each " \
              "participant in your house." \
              "You many provide a house as an argument to look up their " \
              "points." \
              "\n\nExamples: `%shousepoints`, `%shousepoints slytherin`" % (
                  prefix, prefix)
        embed = discord.Embed(
            title="Show House Points Help",
            color=COLOR,
            description=msg)
    elif arg == "standings":
        msg = "Show the current house rankings. "\
              "\n\nExample: `%sstandings`" % prefix
        embed = discord.Embed(
            title="Standings Help",
            color=COLOR,
            description=msg)
    elif arg == "leaderboard":
        msg = "Show the current rankings of top participants' total points. "\
              "You may provide a category to see the rankings in that. " \
              "Valid categories are `daily`, `post`, `beta`, `workshop`, " \
              "`art`, `comment`, `wc`, `word_count`, `excred`, or `mod_adjust`" \
              "\n\nExamples: `%sleaderboard`, `%sleaderboard post`" % (
                  prefix, prefix)
        embed = discord.Embed(
            title="Show Points Help",
            color=COLOR,
            description=msg)

    # Mod Only commands
    elif arg == "mod":
        msg = "These are all commands that can only be used by mods."
        embed = discord.Embed(
            title="Mod Only Commands Help",
            color=COLOR,
            description=msg)
        if guild_id in COS_SERVERS:
            embed.add_field(
                name="House Cup Commands:",
                value="`award`, `deduct`, `pingeveryone`",
                inline=False)
            embed.add_field(
                name="Voting Monitoring Commands:",
                value="`startmonitoring`, `stopmonitoring`, `showmonitoring`",
                inline=False)
        embed.add_field(
            name="Utility Commands:",
            value="`pickwinner`",
            inline=False)
        if guild_id in COS_SERVERS:
            embed.add_field(
                name="Server Management Commands",
                value="`deleteallhistory`, `deletesomehistory`, `clearchannelnow`, `imprison`, `showimprisoned`, `caption`, `captionshame`",
                inline=False)
        else:
            embed.add_field(
                name="Server Management Commands",
                value="`deleteallhistory`, `deletesomehistory`",
                inline=False)
    elif arg == "award":
        msg = "Mods only: Award points to someone with a mention and the " \
              "amount of points to give." \
              "\n\n Example `%saward @RedHorse 10`" % prefix
        embed = discord.Embed(
            title="Award Points Help",
            color=COLOR,
            description=msg)
    elif arg == "deduct":
        msg = "Mods only: Deduct points from someone with a mention and the " \
              "amount of points to remove." \
              "\n\n Example `%sdeduct @user 10`" % prefix
        embed = discord.Embed(
            title="Deduct Points Help",
            color=COLOR,
            description=msg)
    elif arg == "pingeveryone":
        msg = "Mods only: Ping everyone currently in the House Cup." \
              "\n\n Example `%spingeveryone`" % prefix
        embed = discord.Embed(
            title="Ping Everyone Help",
            color=COLOR,
            description=msg)
    elif arg == "startmonitoring":
        msg = "Mods only: Start monitoring the number of emoji reacts " \
              "on a message. AMOUNT is the number of reactions allowed. " \
              "If too many reactions are put on a message, sigmabot will " \
              "delete the extra emoji as it is added and ping the offending person." \
              "\n\n Example `%sstartmonitoring MESSAGE_ID CHANNEL_ID AMOUNT`" % prefix
        embed = discord.Embed(
            title="Start Monitoring Help",
            color=COLOR,
            description=msg)
    elif arg == "stopmonitoring":
        msg = "Mods only: Stop monitoring the given message." \
              "\n\n Example `%sstopmonitoring MESSAGE_ID`" % prefix
        embed = discord.Embed(
            title="Stop Monitoring Help",
            color=COLOR,
            description=msg)
    elif arg == "showmonitoring":
        msg = "Mods only: Show the message IDs of the current messages " \
              "that sigmabot is monitoring." \
              "\n\n Example `%sshowmonitoring`" % prefix
        embed = discord.Embed(
            title="Show Monitoring Help",
            color=COLOR,
            description=msg)
    elif arg == "pickwinner":
        msg = "Pick a random person that reacted to a given message. " \
              "This will work no matter how many times a person has reacted with equal probability." \
              "\n\n Example `%spickwinner MESSADE_ID CHANNEL_ID`" % prefix
        embed = discord.Embed(
            title="Pick Winner Help",
            color=COLOR,
            description=msg)
    elif arg == "unwelcome":
        msg = "Trigger the function to kick everyone in COS with " \
              "the welcome role that has not chosen a house role and " \
              "has been in the server for more than a week. " \
              "This also removes the welcome role for those that have " \
              "chosen a house role." \
              "\n\n Example `%sunwelcome`" % prefix
        embed = discord.Embed(
            title="Unwelcome Help",
            color=COLOR,
            description=msg)
    elif arg == "deleteallhistory":
        msg = "Delete every message by the mentioned person in the server. " \
              "\n\n Example `%sdeleteallhistory @person`" % prefix
        embed = discord.Embed(
            title="Delete All History Help",
            color=COLOR,
            description=msg)
    elif arg == "deletesomehistory":
        msg = "Delete every message by the mentioned person in the server except " \
              "pinned messages or messages in channels " \
              "with `~deletesomehistory exempt` in the channel topic." \
              "\n\n Example `%sdeletesomehistory @person`" % prefix
        embed = discord.Embed(
            title="Delete Some History Help",
            color=COLOR,
            description=msg)
    elif arg == "deletehistory":
        msg = "Please use `~deleteallhistory` or `~deletesomehistory`.\n\n" \
              "`~deleteallhistory` deletes every message by the person it's being run on.\n" \
              "`~deletesomehistory` does not delete pinned messages or messages in channels " \
              "with `~deletesomehistory exempt` in the channel topic."
        embed = discord.Embed(
            title="Delete History Help",
            color=COLOR,
            description=msg)
    elif arg == "clearchannels":
        msg = "Delete all messages that are more than a week old in " \
              " the personal channels, except for the ones that are pinned. " \
              "\n\n Example `%sclearchannels`" % prefix
        embed = discord.Embed(
            title="Clear Channels Help",
            color=COLOR,
            description=msg)
    elif arg == "clearchannelnow":
        msg = "Delete all messages in the channel this is called from " \
              "that aren't pinned." \
              "\n\nExample: `%sclearchannelnow`"
        embed = discord.Embed(
            title="Clear Channels Help",
            color=COLOR,
            description=msg)
    elif arg == "caption":
        msg = "Chide someone for not captioning their image for a given message ID and channel ID. " \
              "\nFor more info on how to do this, see [this help doc](%s)" \
              "\n\n Example `~caption MESSADE_ID CHANNEL_ID`" % CAPTION_DOC_LINK
        embed = discord.Embed(
            title="Caption Help",
            color=COLOR,
            description=msg)
    elif arg == "captionshame":
        msg = "Like `~caption`, but with a little more oomph." \
              "\nFor more info on how to do this, see [this help doc](%s)" \
              "\n\n Example `~captionshame MESSADE_ID CHANNEL_ID`" % CAPTION_DOC_LINK
        embed = discord.Embed(
            title="Caption Shame Help",
            color=COLOR,
            description=msg)
    elif arg == "imprison":
        msg = "Give someone the mod-pings role automatically when they join COS. " \
              "REASON can be anything, but I recommend including their " \
              "original name and why they're being imprisoned." \
              "\n\n Example `~imprison USER_ID REASON`"
        embed = discord.Embed(
            title="Imprison Help",
            color=COLOR,
            description=msg)
    elif arg == "showimprisoned":
        msg = "View the current list of people that are being monitored " \
              "and why for when they join the server." \
              "\n\n Example `~showimprisoned`"
        embed = discord.Embed(
            title="Show Imprisoned Help",
            color=COLOR,
            description=msg)

    # Fun Commands
    elif arg == "dumbledore":
        msg = "Try it and see. Example: `%sdumbledore`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nWritten and coded by The Amazing CHRain." % prefix
        embed = discord.Embed(
            title="Dumbledore Help",
            color=COLOR,
            description=msg)
    elif arg == "snape":
        msg = "Try it and see. Example: `%ssnape`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nWritten and coded by The Amazing CHRain." % prefix
        embed = discord.Embed(
            title="Snape Help",
            color=COLOR,
            description=msg)
    elif arg == "sneak":
        msg = "Try it and see. Example: `%ssneak`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nQuotes written by The Great Earth." % prefix
        embed = discord.Embed(
            title="Sneak Help",
            color=COLOR,
            description=msg)
    elif arg == "hermione":
        msg = "Try it and see. Example: `%shermione`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nQuotes written by Batsutousai." % prefix
        embed = discord.Embed(
            title="Hermione Help",
            color=COLOR,
            description=msg)
    elif arg == "harry":
        msg = "Try it and see. Example: `%sharry`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nQuotes written by Amino." % prefix
        embed = discord.Embed(
            title="Harry Help",
            color=COLOR,
            description=msg)
    elif arg == "ron":
        msg = "Try it and see. Example: `%sron`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nResponse written by Caty Pie." % prefix
        embed = discord.Embed(
            title="Ron Help",
            color=COLOR,
            description=msg)
    elif arg == "mcgonagall":
        msg = "Try it and see. Example: `%smcgonagall`\n" \
              "Don't worry though, the command is just for fun." \
              "\n\nQuotes written by Batsutousai." % prefix
        embed = discord.Embed(
            title="McGonagall Help",
            color=COLOR,
            description=msg)
    elif arg == "grouphug" or arg == "group_hug" or arg == "hug":
        msg = "Give someone or a group of people a hug! " \
              "Examples: `%shug @catyPi @stuffle`, `%shug chukar`" \
              "\n\nGifs and captions by Stuffle, Chukar, and Caty Pi." % (
                  prefix, prefix)
        embed = discord.Embed(
            title="Hug Help",
            color=COLOR,
            description=msg)
    elif arg == "cheer":
        msg = "Cheer someone on!\n " \
              "Examples: `%scheer person`" % prefix
        embed = discord.Embed(
            title="Cheer Help",
            color=COLOR,
            description=msg)
    elif arg == "kidnap":
        msg = "Kidnap someone! Example: `%skidnap @dorea`" \
              "\n\nMost gifs supplied by Dorea." % prefix
        embed = discord.Embed(
            title="Kidnap Help",
            color=COLOR,
            description=msg)
    elif arg == "wrestle":
        msg = "Wrestle someone to settle a dispute! Example: `%swrestle @red`" \
              "\n\nInspiration and some responses/fluids supplied by " \
              "Red, Earth, Caty, May, Chukar, Mik" % prefix
        embed = discord.Embed(
            title="Wrestle Help",
            color=COLOR,
            description=msg)
    elif arg == "pillage":
        msg = "Go pillaging! Example: `%spillage`" \
              "\n\nMost gifs supplied by Dorea." % prefix
        embed = discord.Embed(
            title="Pillage Help",
            color=COLOR,
            description=msg)

    # Marriage Commands
    elif arg == "marry":
        msg = "Marry another user. With this command you can propose to a " \
              "user, accept a proposal, and remarry.\n\n" \
              "Example: `%smarry @person`" % prefix
        embed = discord.Embed(
            title="Marry Help",
            color=COLOR,
            description=msg)
    elif arg == "marriages":
        msg = "View all of the people you are married to and how many times" \
              " (based on the number of heart emoji next to their name)." \
              "You many mention a person to look up their marriages.\n" \
              "Heart emoji by Sparky and Kami." \
              "\nTo see all marriage commands, view the list of all commands with `~help`." \
              "\n\nExamples: `%smarriages`, `%smarriages @person`" % (prefix, prefix)
        embed = discord.Embed(
            title="Marriages Help",
            color=COLOR,
            description=msg)
    elif arg == "divorce":
        msg = "Divorce someone. If you divorce them enough that your " \
              "marriage count drops below 0, they will show up in your " \
              "marriage list with a broken heart. " \
              "With 0 marriages, they'll disappear." \
              "\n\nExample: `~divorce @person`"
        embed = discord.Embed(
            title="Divorce Help",
            color = COLOR,
            description=msg)

    # Pact Commands
    elif arg == "formpact":
        msg = "Form a pact with another user. " \
              "This will show the promise in `~pacts` until they `~fulfill` or `~acceptfailure`." \
              "\n\nExample: `%sformpact I swear to @person " \
              "that I will write today.`" % prefix
        embed = discord.Embed(
            title="Form Pact Help",
            color=COLOR,
            description=msg)
    elif arg == "pacts" or arg == "pact":
        msg = "View all of the current pacts you or someone else has. " \
              "Idea for the pact system came from RedHorse!" \
              "\nTo see all pact commands, view the list of all commands with `~help`." \
              "\n\nExamples: `%spacts`, `%spacts @person`" % (prefix, prefix)
        embed = discord.Embed(
            title="Pacts Help",
            color=COLOR,
            description=msg)
    elif arg == "completed":
        msg = "View all of the completed pacts you or someone else has. " \
              "\n\nExamples: `~completed`, `~completed @person`"
        embed = discord.Embed(
            title="Completed Pacts Help",
            color=COLOR,
            description=msg)
    elif arg == "failed":
        msg = "View all of the failed pacts you or someone else has. " \
              "\n\nExamples: `~failed`, `~failed @person`"
        embed = discord.Embed(
            title="Pacts Help",
            color=COLOR,
            description=msg)
    elif arg == "fulfill":
        msg = "Release someone from their pact to you by acknowledging that they completed it. " \
              "If they have multiple pacts with you, you will need to " \
              "provide a pact ID, which you can find in `~pacts @person`" \
              "\n\nExamples: `~fulfill @person`, `~fulfill @person 1`"
        embed = discord.Embed(
            title="Fulfill Help",
            color = COLOR,
            description=msg)
    elif arg == "acceptfailure":
        msg = "Release someone from their pact to you that they did not complete. " \
              "If they have multiple pacts with you, you will need to " \
              "provide a pact ID, which you can find in `~pacts @person`" \
              "\n\nExamples: `~acceptfailure @person`, `~acceptfailure @person 1`"
        embed = discord.Embed(
            title="Accept Failure Help",
            color = COLOR,
            description=msg)

    # Identity Commands
    elif arg == "whois":
        msg = "View the identity of someone who has been registered with `~identify`. " \
              "This function takes either the first word of a display name, a user ID or a mention.\n" \
              "You can get a person's user ID by turning on Discord's developer mode. " \
              "Further instructions available here: " \
              "https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-\n" \
              "This command is private to CSUA servers." \
              "\n\nExamples: `~whois USER_ID`, `~whois @person`, `~whois name`"
        embed = discord.Embed(
            title="Whois Help",
            color=COLOR,
            description=msg)
    elif arg == "identify":
        msg = "Set someone's identity so that it can be looked up with `~whois`. " \
              "This command is private to CSUA servers. " \
              "Be informative enough that people can actually figure out who you are. " \
              "Please provide a mention as the first argument. " \
              "\n\nExamples: `~identify @stufflebear Mary, og CSUA, class of 2013`\n" \
              "`~identify @me Name, X's friend from Berkeley who you might have met at CSUA parties`"
        embed = discord.Embed(
            title="Identify Help",
            color=COLOR,
            description=msg)

    # Writing Commands
    elif arg == "prompt":
        msg = "Get a randomly generated prompt. Example: `%sprompt`" \
              "\n\nPrompt options written by RedHorse, Stuffle, " \
              "Aubry, Essa, Mik, and DarkBlue\n" % prefix
        embed = discord.Embed(
            title="Prompt Help",
            color=COLOR,
            description=msg)
    elif arg == "inspireme":
        msg = "Get some inspiration from sigmabot. Example: `%sinspireme`" \
              "\n\nResponses written by Caty, Dorea, Red, Essa, and Stuffle." % prefix
        embed = discord.Embed(
            title="InspireMe Help",
            color=COLOR,
            description=msg)
    elif arg.startswith("shouldikill"):
        msg = "Have sigmabot decide if you should kill your character. " \
              "Example: `%sshouldikillmycharacter`" % prefix
        embed = discord.Embed(
            title="ShouldIKillMyCharacter Help",
            color=COLOR,
            description=msg)
    elif arg == "shouldigetbacktowork":
        msg = "Ask sigmabot if you should get back to work.\n\n" \
              "Example: `%sshouldigetbacktowork`" % prefix
        embed = discord.Embed(
            title="shouldIGetBacktoWork Help",
            color=COLOR,
            description=msg)
    elif arg == "whenshouldtheyfuck":
        msg = "Ask sigmabot when your characters should fuck. " \
              "Most responses written by Red.\n\n" \
              "Example: `%swhenshouldtheyfuck`" % prefix
        embed = discord.Embed(
            title="WhenShouldTheyFuck Help",
            color=COLOR,
            description=msg)
    elif arg == "randompair":
        msg = "Have sigmabot give you a random pairing.\n\n" \
              "Example: `%srandompair`" % prefix
        embed = discord.Embed(
            title="RandomPair Help",
            color=COLOR,
            description=msg)
    elif arg == "kink":
        msg = "Have sigmabot give you a random kink.\n\n" \
              "Example: `%skink`" % prefix
        embed = discord.Embed(
            title="Kink Help",
            color=COLOR,
            description=msg)
    elif arg == "iloveyou":
        msg = "Tell sigmabot how much you love it.\n\n" \
              "Example: `%siloveyou`" % prefix
        embed = discord.Embed(
            title="I Love You Help",
            color=COLOR,
            description=msg)
    elif arg == "madness":
        msg = "Get an image of madness. You can direct this at people.\n\n" \
              "Example: `%smadness @person`" % prefix
        embed = discord.Embed(
            title="Madness Help",
            color=COLOR,
            description=msg)

    elif embed is None:
        msg = "Sorry! This command is unrecognized. View the general help " \
              "for a list of commands with `%shelp`." % prefix
        embed = discord.Embed(
            title="Unrecognized Command",
            color=COLOR,
            description=msg)

    return embed


def general_help(prefix, guild_id):
    msg = "Commands list. For help on a specific command, run " \
          "`~help COMMAND`."
    if guild_id in COS_SERVERS:
        msg = msg + "\nDocumentation on how the bot and competition work" \
                     " are available [here](%s)." % DOCS_LINK

    embed = discord.Embed(
        title="SigmaBot Help",
        color=COLOR,
        description=msg)

    if guild_id in COS_SERVERS:
        embed.add_field(
            name="House Cup:",
            value="Participating: `join`, `leave`, `time`\n"
                  "Logging Points: `daily`, `post`, `beta`, `art`, `comment`, `workshop`, `exercise`, `excred`, `wc` (total), `wc add`, `remove`, `sneak`\n"
                  "Viewing Points: `points`, `standings`, `housepoints`, `leaderboard`",
            inline=False)
        embed.add_field(
            name="Marriage Commands:",
            value="`marry`, `divorce`, `marriages`",
            inline=False)

    if guild_id in CSUA_SERVERS:
        embed.add_field(
            name="Identity Commands:",
            value="`whois`, `identify`",
            inline=False)


    embed.add_field(
        name="Pact Commands:",
        value="Managing Pacts: `formpact`, `fulfill`, `acceptfailure`\n" \
              "Viewing Pacts: `pacts`, `completed`, `failed`",
        inline=False)
    embed.add_field(
        name="Action Commands:",
        value="`hug`, `cheer`, `kidnap`, `pillage`, `wrestle`",
        inline=False)
    embed.add_field(
        name="Harry Potter Commands:",
        value="`prompt`, `randompair`, `dumbledore`, `snape`, `mcgonagall`, `harry`, `hermione`, `ron`",
        inline=False)
    embed.add_field(
        name="Inspiration Commands:",
        value="`inspireme`, `shouldikillmycharacter`, `shouldigetbacktowork`, `whenshouldtheyfuck`",
        inline=False)
    embed.add_field(
        name="For More Commands:",
        value="Mod only commands: `help mod`",
        inline=False)

    return embed
