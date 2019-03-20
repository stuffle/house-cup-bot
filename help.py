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
        msg = "Join the house cup with your current house role. \n" \
              "Unless you leave and rejoin, you will have your current" \
              " house and name for the entirety of the month."
        embed = discord.Embed(
            title="Join Help",
            color=COLOR,
            description=msg)
    elif embed == None:
        msg = "Sorry! It may be because stuffle is still writing the help command."
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
