# Work with Python 3.6
import discord
import asyncio
import ast
import os
import re
import random

from humor_commands import *


SLYTHERIN = "slytherin"
RAVENCLAW = "ravenclaw"
GRYFFINDOR = "gryffindor"
HUFFLEPUFF = "hufflepuff"
HOUSES = [SLYTHERIN, GRYFFINDOR, RAVENCLAW, HUFFLEPUFF]
HOUSE_TO_EMOJI = {
    SLYTHERIN: ":snake:",
    RAVENCLAW: ":eagle:",
    GRYFFINDOR: ":lion:",
    HUFFLEPUFF: ":hugging:"
}
HOUSE_TO_HEART = {
    SLYTHERIN: ":green_heart:",
    RAVENCLAW: ":blue_heart:",
    GRYFFINDOR: ":heart:",
    HUFFLEPUFF: ":yellow_heart:"
}

DAILY = "daily"
POST = "post"
BETA = "beta"
WORKSHOP = "workshop"
COMMENT = "comment"
EXCRED = "excred"
CATEGORIES = [DAILY, POST, BETA, WORKSHOP, COMMENT, EXCRED]
CATEGORY_TO_POINTS = {
    DAILY: 5,
    POST: 10,
    BETA: 10,
    WORKSHOP: 30,
    COMMENT: 5
}
VALID_CATEGORIES = "Valid arguments to this command are `daily`, `post`," \
                   " `beta`, `workshop`, `comment`, and `excred`"

DOCS_LINK = "https://docs.google.com/document/d/1z03xR7jpi-oXwmI9N1XpU6N9" \
            "0BnXmj5ptyASdWnIkNA/edit?usp=sharing"

client = discord.Client()
participants = {}


def load_participants():
    global participants

    with open("data.json", encoding='utf-8') as f:
        file_text = f.read()
        participants = ast.literal_eval(file_text)


def save_participants():
    with open("data.json", 'w', encoding='utf-8') as f:
        f.write(str(participants))


def get_house(user):
    user_id = user.id

    if user_id in participants.keys():
        return participants[user_id]["house"]

    role_names = [role.name.lower() for role in user.roles]

    house = ""
    houses = 0
    if SLYTHERIN in role_names:
        house = SLYTHERIN
        houses += 1
    if RAVENCLAW in role_names:
        house = RAVENCLAW
        houses += 1
    if GRYFFINDOR in role_names:
        house = GRYFFINDOR
        houses += 1
    if HUFFLEPUFF in role_names:
        house = HUFFLEPUFF
        houses += 1

    if houses == 0:
        raise Exception(
            "You need to join a house to participate in the house cup.")
    if houses > 1:
        raise Exception(
            "You cannot participate in the house cup with multiple house roles.")

    return house


def get_paticipants(house):
    members = []
    for p in participants:
        member = participants[p]
        if member["house"] == house:
            members.append(member)
    return members


def sort_participants(members, category):
    """
    Returns a list of (participant, points)
    """
    members_and_points = []
    for member in members:
        points = 0
        if category == "total":
            points = calculate_personal_score(
                get_userid_from_mention(member["mention"]))
        else:
            points = member[category]
        members_and_points.append((member, points))
    return sorted(members_and_points, key=lambda tup: tup[1], reverse=True)


def get_userid_from_mention(mention):
    user_id = re.sub('[!<>@]', '', mention)
    return user_id


def calculate_personal_score(user_id):
    p = participants[user_id]
    core_points = p["daily"] + p["post"] + p["beta"]
    return core_points + p["workshop"] + p["comment"] + p["excred"]


def format_name(number, name):
    formatted_number = "**" + str(number) + "** "
    formatted_name = "`" + name.capitalize() + "`: "
    return formatted_number + formatted_name


def join(user):
    """
    TODO: Implement deadline for joining
    """
    if user.id in participants.keys():
        raise Exception(
            "You have already joined the house cup for this month.")

    house = get_house(user)

    participant = {
        "name": user.name,
        "mention": user.mention,
        "house": house,
        "daily": 0,
        "post": 0,
        "beta": 0,
        "workshop": 0,
        "comment": 0,
        "excred": 0
    }

    participants[user.id] = participant

    return "Welcome to the House Cup {0.author.mention}! " \
           "May the odds be ever in " + house.capitalize() + "'s favor."


def leave(user):
    msg = "{0.author.mention}: You can check out any time you like. " \
          "But you can never leave! :musical_note: \n\n" \
          "But if you insist, know that your score will be wiped out. " \
          "Use  `~actuallyleave`  :sob:"
    return msg


def actually_leave(user):
    if user.id not in participants:
        raise Exception("You can't leave a contest you're not in.")

    del participants[user.id]

    msg = "{0.author.mention}: You have left the house cup. :sob:\n" \
          "To rejoin (if it's not too late), use `~join`"
    return msg


def log_score(text, user):
    """
    Record house points.

    Text example: `~log excred 20`
    """
    msg = ""
    print("Running log")
    args = text.split()
    amount = 0

    if user.id not in participants:
        raise Exception("Please join the house cup with `~join`")

    house = participants[user.id]["house"].capitalize()

    # Check if valid inputs
    if len(args) < 2:
        raise Exception(
            "Please provide a category to log your points in. " + VALID_CATEGORIES)

    category = args[1].lower()
    if category not in CATEGORIES:
        raise Exception("Unrecognized Category. " + VALID_CATEGORIES)

    if category != EXCRED:
        points = CATEGORY_TO_POINTS[category]
        participants[user.id][category] = participants[user.id][category] + points

    # Add points where appropriate
    if category == DAILY:
        msg = "Congratulations on doing something today—" \
              "take 5 points for " + house + "! " + HOUSE_TO_HEART[house.lower()]
    if category == POST:
        msg = "YESSS!!! :eyes: :eyes: 10 points to " + house + "!"
    if category == BETA:
        msg = "You're a better beta than Harry is an omega. :wink:\n" \
              "10 points to " + house + "!"
    if category == WORKSHOP:
        msg = "Thank you for putting your work up for the weekly workshop " \
              "~~gangbang~~. Take a whopping 30 points for " + house + "!"
    if category == COMMENT:
        msg = "Comments are so appreciated. :sparkling_heart: 5 points to" \
              " " + house + "!"
    if category == EXCRED:
        if len(args) <= 2:
            raise Exception(
                "Please provide an amount for the extra credit, like `~excred 10`")
        if not args[2].isdigit():
            raise Exception(
                "Extra credit amount must be a number. Try something like `~excred 10`")
        amount = int(args[2])
        new_excred_total = participants[user.id][EXCRED] + amount
        if new_excred_total >= 50:
            new_excred_total = 50
            msg = "Your extra credit score has been set to the maximum, 50." \
                  " Thank you for contributing so much! :heart:"
        elif amount == 0:
            raise Exception(
                "Please provide the amount of extra credit points earned. For example: `~excred 20`")
        else:
            msg = str(amount) + " points to " + house + " for extra credit work!"
        participants[user.id][EXCRED] = new_excred_total

    return msg


def remove_score(text, user):
    msg = ""
    print("Running remove")
    args = text.split()
    amount = 0

    if user.id not in participants:
        raise Exception("You can't remove points because you're not in the house cup. :sob:")

    house = participants[user.id]["house"].capitalize()

    # Check if valid inputs
    if len(args) < 2:
        raise Exception(
            "Please provide a category to remove points from " + VALID_CATEGORIES)

    category = args[1].lower()
    if category not in CATEGORIES:
        raise Exception("Unrecognized Category. " + VALID_CATEGORIES)

    points = 0
    if category == EXCRED:
        if len(args) <= 2:
            raise Exception(
                "Please provide an amount for the extra credit, like `~remove excred 10`")
        if not args[2].isdigit():
            raise Exception(
                "Extra credit amount must be a number. Try something like `~remove excred 10`")
        amount = int(args[2])
        if amount <= 0:
            raise Exception(
                "Please provide the amount of extra credit points to remove as a positive integer. For example: `~remove excred 20`")
        points = amount
    else:
        points = CATEGORY_TO_POINTS[category]
    new_points = participants[user.id][category] - points
    if new_points < 0:
        raise("No points were taken from you because this would set your total in " + str(category).capitalize() + " to a negative number.")
    else:
        participants[user.id][category] = new_points
        msg = str(points) + " points were removed from " + house + ". RIP."

    return msg


def points(user, message):
    text = message.content
    args = text.split()
    person_id = user.id
    person_mention = user.mention
    msg = ""

    if len(message.mentions) == 1:
        person_id = message.mentions[0].id
        person_mention = message.mentions[0].mention
    elif len(message.mentions) > 1:
        raise Exception(
            "You can only look up the points of one user at a time.")
    elif len(args) > 1 and len(message.mentions) == 0:
        raise Exception(
            "In order to look up the points of someone else, you must mention them. For example: `~points @person`. Or, to look at your own score, use `~ponts`")

    if person_id not in participants:
        raise Exception(
            person_mention + " is not currently participating in the house cup. :sob:")

    person = participants[person_id]

    who_message = person_mention + "'s points are:"
    total_message = "__**Total:  " + str(
        calculate_personal_score(person_id)) + "**__"
    daily_message = format_name(
        ":white_sun_small_cloud:", DAILY) + str(person[DAILY])
    post_message = format_name(":book:", POST) + str(person[POST])
    beta_message = format_name(":pencil:", BETA) + str(person[BETA])
    comment_message = format_name(":keyboard:", COMMENT) + str(person[COMMENT])
    workshop_message = format_name(
        ":sweat_smile:", WORKSHOP) + str(person[WORKSHOP])
    excred_message = format_name(":avocado:", EXCRED) + str(person[EXCRED])

    msg = "\n".join([who_message, total_message, daily_message, post_message,
                     beta_message, comment_message, workshop_message,
                     excred_message])
    return msg


def house_points(user, message):
    text = message.content
    args = text.split()
    house = get_house(user)
    msg = ""

    if len(args) > 1:
        possible_house = args[1]
        if possible_house not in HOUSES:
            raise Exception(possible_house + " is not a valid house. Try `~housepoints slytherin`")
        else:
            house = possible_house

    # Sort by total points
    members = get_paticipants(house)
    sorted_members = sort_participants(members, "total")

    # TODO: Use real house total based on points calculation
    house_total = calculate_house_score(house)
    heart = HOUSE_TO_HEART[house] + " "
    house_title = heart + "__**" + house.capitalize() + ":** "
    msg = house_title + str(house_total) + "__ " + heart + "\n"

    # Add each member to return message
    rank = 1
    for member, total_points in sorted_members:
        formatted_name = format_name(rank, member["name"])
        msg = msg + formatted_name + str(total_points) + "\n"
        rank += 1

    emoji_line = HOUSE_TO_EMOJI[house] * 7
    return msg + emoji_line


def leader_board(user, message):
    """
    Show top 5 students in a given category
    """
    text = message.content
    args = text.split()
    house = get_house(user)
    category = "total"
    valid_args = "Valid arguments to `~leaderboard` are `daily`, `post`," \
                 " `beta`, `workshop`, `comment`, `excred`, and `total`"
    msg = ""

    if len(args) > 1:
        category = args[1]
        if category not in CATEGORIES + ["total"]:
            raise Exception(valid_args)

    sorted_members = sort_participants(participants.values(), category)[:5]

    msg = "__**Top 5 Students for " + category.capitalize() + " Points:**__\n"

    # Add each member to return message
    number = 1
    for member, points in sorted_members:
        heart = "  " + HOUSE_TO_HEART[member["house"]]
        formatted_name = format_name(number, member["name"])
        msg = msg + formatted_name + str(points) + heart + "\n"
        number += 1

    return msg


def calculate_house_score(house):
    house_score = 0.0
    members = get_paticipants(house)
    sorted_members = sort_participants(members, "total")
    sorted_points = [x[1] for x in sorted_members]

    while len(sorted_points) < 3:
        sorted_points.append(0)

    for index, points in enumerate(sorted_points):
        iteration = index + 1
        denominator = 2**iteration

        """
        If we're on the last iteration, use the previous number in the
        geometric sum so that the weights sum to 1
         """
        if iteration == len(sorted_points):
            denominator = 2**index

        weight = 1 / denominator
        house_score += weight * float(points)

    return house_score


def standings():
    house_and_score = []
    for house in HOUSES:
        score = calculate_house_score(house)
        house_and_score.append((house, score))

    sorted_houses = sorted(
        house_and_score, key=lambda tup: tup[1], reverse=True)
    first_place_house, first_place_score = sorted_houses[0]
    heart = HOUSE_TO_HEART[first_place_house]
    winners_emoji = heart + HOUSE_TO_EMOJI[first_place_house]

    msg = " **__Current Standings:__** " + winners_emoji + "\n"
    number = 1
    for house, score in sorted_houses:
        formatted_house = format_name(number, house)
        msg = msg + formatted_house + str(score) + "\n"
        number += 1

    emoji_line = HOUSE_TO_EMOJI[first_place_house] * 7
    return msg + emoji_line


@client.event
async def on_message(message):
    user = message.author
    mention = user.mention
    text = message.content.lower()
    msg = ""

    # Prevent the bot from replying to itself
    if user == client.user:
        return

    # Ignore all messages not directed at bot
    if not message.content.startswith("~"):
        return

    try:
        if text == "~join":
            msg = join(user)
            save_participants()
            print(participants)

        elif text.startswith("~leave"):
            msg = leave(user)

        elif text.startswith("~actuallyleave"):
            msg = actually_leave(user)
            save_participants()

        elif text.startswith("~log"):
            msg = "{0.author.mention}: " + log_score(text, user)
            save_participants()

        elif text.startswith("~daily"):
            msg = "{0.author.mention}: " + log_score("~log daily", user)
            save_participants()

        elif text.startswith("~post"):
            msg = "{0.author.mention}: " + log_score("~log post", user)
            save_participants()

        elif text.startswith("~beta"):
            msg = "{0.author.mention}: " + log_score("~log beta", user)
            save_participants()

        elif text.startswith("~comment"):
            msg = "{0.author.mention}: " + log_score("~log comment", user)
            save_participants()

        elif text.startswith("~workshop"):
            msg = "{0.author.mention}: " + log_score("~log workshop", user)
            save_participants()

        elif text.startswith("~excred"):
            msg = "{0.author.mention}: " + log_score(
                  "~log " + text[1:], user)
            save_participants()

        elif text.startswith("~remove"):
            msg = "{0.author.mention}: " + remove_score(text, user)
            save_participants()

        elif text.startswith("~points"):
            msg = points(user, message)

        elif text.startswith("~housepoints"):
            msg = house_points(user, message)

        elif text.startswith("~leaderboard"):
            msg = leader_board(user, message)

        elif text.startswith("~standings"):
            msg = standings()

        elif text.startswith("~help"):
            msg = "{0.author.mention}: Instructions on bot usage and the" \
                  " house cup itself are in: " + DOCS_LINK

        elif text.startswith("~dumbledore"):
            house = get_house(user)
            embed = dumbledore(house, mention)
            await client.send_message(message.channel, embed=embed)
            return

        elif text.startswith("~snape"):
            house = get_house(user)
            embed = snape(house, mention)
            await client.send_message(message.channel, embed=embed)
            return

    except Exception as ex:
        msg = "{0.author.mention}: " + str(ex)
        print(str(ex))

    if msg:
        await client.send_message(message.channel, msg.format(message))


async def list_recs():
    await client.wait_until_ready()
    print("Current servers:")
    for server in client.servers:
        print(server.name)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    load_participants()


client.loop.create_task(list_recs())
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
