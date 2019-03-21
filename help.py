import discord


DOCS_LINK = "https://docs.google.com/document/d/1z03xR7jpi-oXwmI9N1XpU6N9" \
            "0BnXmj5ptyASdWnIkNA/edit?usp=sharing"
COLOR = 6554835


def help_command(message):
    text = message.content.lower()
    args = text.split()

    if len(args) == 1:
        return general_help()

    arg = args[1]
    embed = None

    if arg == "join":
        msg = "Join the House Cup with your current house role. \n" \
              "Unless you leave and rejoin, you will have your current" \
              " house and name for the entirety of the month."
        embed = discord.Embed(
            title="Join Help",
            color=COLOR,
            description=msg)
    elif arg == "leave":
        msg = "Leave the House Cup. You will lose every point you've earned."
        embed = discord.Embed(
            title="Leave Help",
            color=COLOR,
            description=msg)

    elif arg == "daily":
        msg = "Log 5 points for doing any sort of creative work. " \
              "It doesn't matter how little or how much you did. " \
              "Anything counts. :heart:\n\n" \
              "You must log your days work within 24 hours of doing it."
        embed = discord.Embed(
            title="Daily Help",
            color=COLOR,
            description=msg)
    elif arg == "post":
        msg = "Log 10 points each time you post artwork, " \
              "update a chaptered work, post a new work, " \
              "or help with the bot."
        embed = discord.Embed(
            title="Post Help",
            color=COLOR,
            description=msg)
    elif arg == "beta":
        msg = "Log 10 points each time you beta read a work, " \
              "or participate in a workshop as a reader."
        embed = discord.Embed(
            title="Beta Help",
            color=COLOR,
            description=msg)
    elif arg == "workshop":
        msg = "Log 30 points when you contribute a work to the weekly " \
              "workshop."
        embed = discord.Embed(
            title="Workshop Help",
            color=COLOR,
            description=msg)
    elif arg == "comment":
        # TODO: Update with new criteria
        msg = "Comment: 5 points per comment which meets the following criteria: provides analysis and/or relates to at least 3 specific details of the work."
        embed = discord.Embed(
            title="Comment Help",
            color=COLOR,
            description=msg)
    elif arg == "excred":
        msg = "Use `excred AMOUNT`, where amount is a positive number.\n\n" \
              "Check the House Cup channel for the month's extra credit " \
              "challenge and its corresponding points. " \
              "Maximum Extra Credit is 50 points per month."
        embed = discord.Embed(
            title="Extra Credit Help",
            color=COLOR,
            description=msg)
    elif arg == "remove":
        msg = "Use `remove CATEGORY` to remove points from a given category. "\
              "CATEGORY may be `daily`, `post`, `beta`, `workshop`, " \
              "`comment`, or `excred`. If you are removing extra credit " \
              "points, you must provide the ammount of points to remove. " \
              "\n\nExamples: `remove daily`, `remove excred 10`"
        embed = discord.Embed(
            title="Remove Points Help",
            color=COLOR,
            description=msg)

    elif arg == "points":
        msg = "Show how many of each kind of point you have. "\
              "You many mention a person to look up their points." \
              "\n\nExamples: `points`, `points @Earth`"
        embed = discord.Embed(
            title="Show Points Help",
            color=COLOR,
            description=msg)
    elif arg == "housepoints":
        msg = "Show your total house points and the points of each " \
              "participant in your house." \
              "You many provide a house as an argument to look up their " \
              "points." \
              "\n\nExamples: `housepoints`, `housepoints slytherin`"
        embed = discord.Embed(
            title="Show House Points Help",
            color=COLOR,
            description=msg)
    elif arg == "standings":
        msg = "Show the current house rankings. "\
              "\n\nExample: `standings`"
        embed = discord.Embed(
            title="Standings Help",
            color=COLOR,
            description=msg)
    elif arg == "leaderboard":
        msg = "Show the current rankings of top participant's total points. "\
              "You mat provide a category to see the rankings in that. " \
              "Valid categories are `daily`, `post`, `beta`, `workshop`, " \
              "`comment`, `excred`, or `mod_adjust`" \
              "\n\nExamples: `leaderboard`, `leaderboard post`"
        embed = discord.Embed(
            title="Show Points Help",
            color=COLOR,
            description=msg)

    elif embed is None:
        msg = "Sorry! It may be because stuffle is still writing " \
              "the help command."
        embed = discord.Embed(
            title="Unrecognized Command",
            color=COLOR,
            description=msg)

    return embed



def general_help():
    msg = "Commands list. For help on a specific command, run " \
          "`~help [command]`.\n" \
          "Documentation on how the bot and competition work are " \
          "available [here](" + DOCS_LINK + ")."

    embed = discord.Embed(
        title="StuffleBot Help",
        color=COLOR,
        description=msg)

    embed.add_field(
        name="Participating:",
        value="`join`, `leave`",
        inline=False)
    embed.add_field(
        name="Logging Points:",
        value="`daily`, `post`, `beta`, `comment`, `workshop`, `excred`, `remove`",
        inline=False)
    embed.add_field(
        name="Viewing Points:",
        value="`points`, `standings`, `housepoints`, `leaderboard`",
        inline=False)
    embed.add_field(
        name="Mod Only Commands:",
        value="`award`, `deduct`",
        inline=False)
    embed.add_field(
        name="Fun Commands:",
        value="`dumbledore`, `snape`",
        inline=False)

    return embed
