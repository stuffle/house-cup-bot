# Work with Python 3.6
import discord
import asyncio
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import ast
import os
import re
import random
import time
from calendar import monthrange
import datetime

from humor_commands import *
from help import *


IS_TEST_ENV = os.environ.get("IS_TEST_ENV")
PREFIX = "~"
if IS_TEST_ENV:
    PREFIX = "$"
DATA_FILE = "data.json"
if IS_TEST_ENV:
    DATA_FILE = "test_data.json"

SLYTHERIN = "slytherin"
RAVENCLAW = "ravenclaw"
GRYFFINDOR = "gryffindor"
HUFFLEPUFF = "hufflepuff"
HOUSES = [SLYTHERIN, GRYFFINDOR, RAVENCLAW, HUFFLEPUFF]
HOUSE_TO_EMOJI = {
    SLYTHERIN: ":snake:",
    RAVENCLAW: ":eagle:",
    GRYFFINDOR: ":lion:",
    HUFFLEPUFF: ":unicorn:"
}
HOUSE_TO_HEART = {
    SLYTHERIN: ":green_heart:",
    RAVENCLAW: ":blue_heart:",
    GRYFFINDOR: ":heart:",
    HUFFLEPUFF: ":yellow_heart:"
}
HOUSE_TO_ADJECTIVE = {
    SLYTHERIN: "cunning",
    RAVENCLAW: "wise",
    GRYFFINDOR: "brave",
    HUFFLEPUFF: "loyal"
}

DAILY = "daily"
POST = "post"
BETA = "beta"
WORKSHOP = "workshop"
COMMENT = "comment"
EXCRED = "excred"
MOD_ADJUST = "mod_adjust"
WC = "wc"
CATEGORIES = [DAILY, POST, BETA, WORKSHOP, COMMENT, WC, EXCRED, MOD_ADJUST]
CATEGORY_TO_POINTS = {
    DAILY: 5,
    POST: 10,
    BETA: 10,
    WORKSHOP: 30,
    COMMENT: 1
}
CATEGORY_TO_EMOJI = {
    "total": ":trophy:",
    DAILY: ":white_sun_small_cloud:",
    POST: ":book:",
    BETA: ":pencil:",
    COMMENT: ":keyboard:",
    WORKSHOP: ":sweat_smile:",
    EXCRED: ":star2:",
    MOD_ADJUST: ":innocent:",
    WC: ":chart_with_upwards_trend:",
    "word_count": ":books:"
}
VALID_CATEGORIES = "Valid arguments to this command are `daily`, `post`," \
                   " `beta`, `workshop`, `comment`, `wc`, and `excred`"

SERVER_ID_TO_CHANNEL = {
    # Red's Writing Hood: house-cup-bot
    "497039992401428498": "553382529521025037",
    # Test: general
    "539932855845781524": "539932855845781530",
    # COS: bot-spam
    "426319059009798146": "426322538944266240"
}


client = discord.Client()
participants = {}
CAN_JOIN = False


class HouseCupException(Exception):
    pass


def load_participants():
    global participants

    with open(DATA_FILE, encoding='utf-8') as f:
        file_text = f.read()
        participants = ast.literal_eval(file_text)


def save_participants():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(str(participants))


def is_mod(user, channel):
    stuffle_id = "438450978690433024"
    user_is_mod = user.permissions_in(channel).administrator
    role_names = [role.name.lower() for role in user.roles]
    mod_role = "mod" in role_names
    return user_is_mod or mod_role or user.id == stuffle_id


def get_random_person(user):
    """
    Return the name of a random person other than the user.
    """
    members = list(participants.keys())
    if len(members) < 2:
        return "Cedric Diggory"

    person_id = user.id
    person = "Cedric Diggory"
    while person_id == user.id:
        person_id = random.choice(members)
        person = participants[person_id]["name"]
    return person


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
        raise HouseCupException(
            "You need to join a house to participate in the house cup.")
    if houses > 1:
        raise HouseCupException(
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
        elif category in member:
            points = member[category]
        members_and_points.append((member, points))
    return sorted(members_and_points, key=lambda tup: tup[1], reverse=True)


def get_userid_from_mention(mention):
    user_id = re.sub('[!<>@]', '', mention)
    return user_id


def calculate_personal_score(user_id):
    p = participants[user_id]
    core_points = p[DAILY] + p[POST] + p[BETA] + p[WORKSHOP] + p[COMMENT]
    return core_points + p[WC] + p[EXCRED] + p[MOD_ADJUST]


def format_name(number, name):
    formatted_number = "**" + str(number) + "** "
    formatted_name = "`" + name.capitalize() + "`: "
    return formatted_number + formatted_name


def join(user):
    if user.id in participants.keys():
        raise HouseCupException(
            "You have already joined the house cup for this month.")

    # TODO: Is this UTC?
    now = datetime.datetime.now()
    day_of_month = now.day
    _, days_in_month = monthrange(now.year, now.month)
    if not CAN_JOIN and days_in_month - day_of_month <= 7:
        raise HouseCupException(
            "I'm sorry, but it is too late to join the House Cup. "
            "Registration closed a week before the end of the month. "
            "Please come back next month and we will welcome you "
            "with open arms. :hugging:")

    house = get_house(user)

    participant = {
        "name": user.name,
        "mention": user.mention,
        "house": house,
        "last_daily": 0,
        "last_workshop": 0,
        "word_count": 0,  # The actual word count
        DAILY: 0,
        POST: 0,
        BETA: 0,
        WORKSHOP: 0,
        COMMENT: 0,
        EXCRED: 0,
        WC: 0,  # Points earned for word count
        MOD_ADJUST: 0
    }

    participants[user.id] = participant

    return "Welcome to the House Cup {0.author.mention}! " \
           "May the odds be ever in " + house.capitalize() + "'s favor."


def leave(user, message):
    current_points = points(user, message)
    msg = "Are you sure you want to leave the House Cup?" \
          "If you do, your score will be wiped out. " \
          "\n%s\n\n" \
          "If you're sure you want to leave, " \
          "use  `%sactuallyleave`" % (current_points, PREFIX)
    return msg


def actually_leave(user):
    if user.id not in participants:
        raise HouseCupException("You can't leave a contest you're not in.")

    del participants[user.id]

    msg = "{0.author.mention}: You have left the house cup. " \
          "If you have a change of heart, talk to a mod!"
    return msg


def log_score(text, user):
    """
    Record house points.

    Text example: `~log excred 20`
    """
    msg = ""
    args = text.split()
    amount = 0
    quotes = []

    if user.id not in participants:
        raise HouseCupException(
            "Please join the house cup with `" + PREFIX + "join`")

    house = participants[user.id]["house"].capitalize()
    heart = HOUSE_TO_HEART[house.lower()]

    # Check if valid inputs
    if len(args) < 2:
        raise HouseCupException(
            "Please provide a category to log your points in. " + VALID_CATEGORIES)

    category = args[1].lower()
    if category not in CATEGORIES + ["exercise"]:
        raise HouseCupException("Unrecognized Category. " + VALID_CATEGORIES)

    if category == MOD_ADJUST:
        raise HouseCupException(
            "You may not log mod_adjust points, only mods can do that with "
            "`%saward` and `%sdeduct`." % (PREFIX, PREFIX))

    if category not in [EXCRED, COMMENT, DAILY, WORKSHOP, WC, "exercise"]:
        points = CATEGORY_TO_POINTS[category]
        participants[user.id][category] = participants[user.id][category] + points

    # Add points where appropriate
    if category == DAILY:
        msg = "Congratulations on doing something productive today—" \
              "take 5 points for " + house + "! " + heart
        current_points = participants[user.id][DAILY] + 5
        today = datetime.date.today()
        _, days_in_month = monthrange(today.year, today.month)
        if current_points >= 5 * (days_in_month + 1):
            raise HouseCupException(
                "This daily was not logged because then you would have "
                "more dailies than there are days in the month.")

        last_daily = 0
        if "last_daily" in participants[user.id].keys():
            last_daily = participants[user.id]["last_daily"]
        now = time.time()
        eight_hours = 14400 * 2  # seconds
        if last_daily + eight_hours > now:
            raise HouseCupException(
                "Please adhere to the rules of only using this "
                "command once per day and only for days that you have been "
                "creatively productive.")
        participants[user.id][DAILY] = current_points
        participants[user.id]["last_daily"] = now

    if category == POST:
        # Mean
        quotes.append(
            "10 points to %s. It took you a while, didn't it? "
            "But really, what else could I expect from a %s? "
            "Anyways, please update again soon." % (house, house))
        # Nice
        quotes.append(
            "Nice work! The fandom appreciates your contribution. "
            "%s 10 points to %s!" % (heart, house))
        quotes.append("YESSS!!! :eyes: 10 points to %s!" % house)
        quotes.append(
            "I'm glad that you're sharing your work with us. "
            "10 points to %s!" % house)
        quotes.append(
            "We're always happy to see your updates. "
            "10 points to %s!" % house)

    if category == BETA:
        quotes.append(
            "You're a better beta than Harry is an omega. "
            "10 points to %s!" % house)
        quotes.append(
            "Betaing is an important job, and you do it well. "
            "10 points to %s!" % house)
        quotes.append(
            "Thank you for helping someone improve their fic. "
            "It's not just them who appreciate you; "
            "it's all of us, for giving us a better fic to read. "
            "Take a well-deserved 10 points.")
    if category == "exercise":
        msg = "Thanks for participating in a weekly exercise! Take 5 " \
              "workshop points for %s!" % house
        participants[user.id][WORKSHOP] = participants[user.id][WORKSHOP] + 5

    if category == WORKSHOP:
        msg = "Thank you for putting your work up for the weekly workshop " \
              "~~gangbang~~. Take a whopping 30 points for " + house + "!"
        last_workshop = 0
        if "last_workshop" in participants[user.id].keys():
            last_workshop = participants[user.id]["last_workshop"]
        now = time.time()
        one_day = 86400  # seconds
        if last_workshop + one_day > now:
            raise HouseCupException(
                "You may only log a workshop once per day. "
                "You must wait 24 hours between logging workshops.")
        participants[user.id][WORKSHOP] = participants[user.id][WORKSHOP] + 30
        participants[user.id]["last_workshop"] = now
    if category == COMMENT:
        if len(args) < 3:
            msg = "Comments are so appreciated. :revolving_hearts: 1 point to"\
                  " " + house + "!"
            participants[user.id][COMMENT] = participants[user.id][COMMENT] + 1
        elif args[2] in ["extra", "essay", "long", "mystery"]:
            msg = "You've probably made someone really happy with your long " \
                  "and thoughtful comment! Good job! :sparkling_heart: " \
                  "5 points to " + house + "!"
            participants[user.id][COMMENT] = participants[user.id][COMMENT] + 5
        else:
            raise HouseCupException(
                "Unrecognized argument to `%scomment`. For a regular comment, "
                "do `%scomment`. For an essay length comment, do "
                "`%scomment extra`" % (PREFIX, PREFIX, PREFIX))

    if category == WC:
        wordcount = 0
        wc_points = 0
        amount = 0
        if "word_count" in participants[user.id]:
            wordcount = participants[user.id]["word_count"]
        if WC in participants[user.id]:
            wc_points = participants[user.id][WC]
        if len(args) <= 2:
            raise HouseCupException(
                "`%swc` takes arguments. Do something like "
                "`%swc 9000` to set your total word count for the month "
                "or `%swc add 3000` to add to your total." % (
                    PREFIX, PREFIX, PREFIX))
        elif args[2] == "add":
            if len(args) <= 3 or not args[3].isdigit():
                raise HouseCupException(
                    "Please provide a number to add to your total word count."
                    " For example: `%swc add 3000`" % PREFIX)
            amount = int(args[3])
            wordcount = wordcount + amount
        elif not args[2].isdigit():
            raise HouseCupException(
                "Total word count must be a number. Try something like "
                "`%swc 9000` or `%swc add 3000`." % (PREFIX, PREFIX))
        else:  # We have valid "log wc total"
            wordcount = int(args[2])
        wc_points = round(wordcount / 1000)
        plural = "s"
        if wc_points == 1:
            plural = ""
        participants[user.id]["word_count"] = wordcount
        if wc_points >= 25:
            wc_points = 25
            msg = "You have now earned the max number of wc points. " \
                "Thank you for contributing so much writing. %s " % heart
        if args[2] == "add":
            msg = "Congratulations on posting %d words! " \
                "This brings your total  to %d, giving you %d point%s! " % (
                    amount, wordcount, wc_points, plural) + msg
        else:
            msg = "Your total wordcount is now %d, giving you %d point%s! " \
                "Congratulations! " % (wordcount, wc_points, plural) + msg
        participants[user.id][WC] = wc_points

    if category == EXCRED:
        if len(args) <= 2:
            raise HouseCupException(
                "Please provide an amount for the extra credit, like `" + PREFIX + "excred 10`")
        if not args[2].isdigit():
            raise HouseCupException(
                "Extra credit amount must be a number. Try something like `" + PREFIX + "excred 10`")
        amount = int(args[2])
        new_excred_total = participants[user.id][EXCRED] + amount
        if new_excred_total >= 50:
            new_excred_total = 50
            msg = "Your extra credit score has been set to the maximum, 50." \
                  " Thank you for contributing so much! :heart:"
        elif amount == 0:
            raise HouseCupException(
                "Please provide the amount of extra credit points earned. For example: `" + PREFIX + "excred 20`")
        else:
            msg = str(amount) + " points to " + house + " for extra credit work!"
        participants[user.id][EXCRED] = new_excred_total

    # If I still set msg, there is only one possible response
    if msg:
        return msg

    return random.choice(quotes)


def remove_score(text, user):
    msg = ""
    print("Running remove")
    args = text.split()
    amount = 0

    if user.id not in participants:
        raise HouseCupException("You can't remove points because you're not in the house cup. :sob:")

    house = participants[user.id]["house"].capitalize()

    # Check if valid inputs
    if len(args) < 2:
        raise HouseCupException(
            "Please provide a category to remove points from " + VALID_CATEGORIES)

    category = args[1].lower()
    if category == WC:
        raise HouseCupException(
            "Please adjust your wordcount by resetting the "
            "total with `%swc TOTAL`" % PREFIX)
    if category not in CATEGORIES + ["exercise"] or category == MOD_ADJUST:
        raise HouseCupException("Unrecognized Category. " + VALID_CATEGORIES)

    points = 0
    new_points = 0
    if category == EXCRED:
        if len(args) <= 2:
            raise HouseCupException(
                "Please provide an amount for the extra credit, like "
                "`" + PREFIX + "remove excred 10`")
        if not args[2].isdigit():
            raise HouseCupException(
                "Extra credit amount must be a number. "
                "Try something like `" + PREFIX + "remove excred 10`")
        amount = int(args[2])
        if amount <= 0:
            raise HouseCupException(
                "Please provide the amount of extra credit points to "
                "remove as a positive integer. For example: "
                "`" + PREFIX + "remove excred 20`")
        points = amount
        new_points = participants[user.id][EXCRED] - points
    elif category == "exercise":
        points = 5
        new_points = participants[user.id][WORKSHOP] - 5
        category = WORKSHOP
    elif category == "comment" and len(args) > 2:
        if args[2] in ["extra", "essay", "mystery"]:
            points = 5
            new_points = participants[user.id][category] - points
        else:
            raise HouseCupException(
                "If you want to remove a regular comment, do "
                "`%sremove comment`. "
                "If you want to remove an 5 point comment, do "
                "`%sremove comment extra`." % (PREFIX, PREFIX))
    else:
        points = CATEGORY_TO_POINTS[category]
        new_points = participants[user.id][category] - points

    if new_points < 0:
        raise HouseCupException(
            "No points were taken from you because this would set your "
            "total in " + str(category).capitalize() + " to "
            "a negative number.")
    else:
        participants[user.id][category] = new_points
        msg = str(points) + " points were removed from " + house + ". RIP."

    return msg


def get_mention_user(needs_mention, mentions):
    """
    Checks that there is only one mentioned user, if needed,
    and that that person is in the House Cup.
    """
    person_id = 0
    person_mention = None

    if len(mentions) == 1:
        person_id = mentions[0].id
        person_mention = mentions[0]
    elif len(mentions) > 1:
        raise HouseCupException(
            "You can only look up the points of one user at a time.")
    elif not needs_mention:
        return None
    elif len(mentions) == 0:
        raise HouseCupException(
            "You must mention someone to use this command.")

    if person_id not in participants:
        raise HouseCupException(
            person_mention.mention + " is not currently participating in the house cup. :sob:")

    return person_mention


def award(user, message):
    text = message.content
    args = text.split()
    msg = ""

    user_is_mod = is_mod(user, message.channel)
    if not user_is_mod:
        raise HouseCupException(
            "Nice try, but only mods can award other people points.")

    award_error = "Please provide a user mention and an amount of points, " \
                  "eg `" + PREFIX + "award @RedHorse 10`"

    if len(args) != 3:
        raise HouseCupException(award_error)

    person_id = user.id
    person_mention = user.mention

    mentioned = get_mention_user(True, message.mentions)
    if mentioned:
        person_id = mentioned.id
        person_mention = mentioned.mention

    if not args[2].isdigit():
        raise HouseCupException(award_error)
    amount = int(args[2])

    new_amount = participants[person_id][MOD_ADJUST] + amount
    participants[person_id][MOD_ADJUST] = new_amount

    house = participants[person_id]["house"]
    adjective = HOUSE_TO_ADJECTIVE[house]
    msg = "The Mods have spoken, and " + str(amount) + " " \
        "points have been awarded to " + house.capitalize() + " for" \
        " " + person_mention + "'s " + adjective + " service."
    return msg


def deduct(user, message):
    """
    Mostly copy pasted from award.
    """
    text = message.content
    args = text.split()
    msg = ""

    user_is_mod = is_mod(user, message.channel)
    if not user_is_mod:
        raise HouseCupException(
            "Nice try, but only mods can deduct other people's points.")

    deduct_error = "Please provide a user mention and an amount of points, " \
                  "eg `" + PREFIX + "deduct @person 10`"

    if len(args) != 3:
        raise HouseCupException(deduct_error)

    person_id = user.id
    person_mention = user.mention

    mentioned = get_mention_user(True, message.mentions)
    if mentioned:
        person_id = mentioned.id
        person_mention = mentioned.mention

    if not args[2].isdigit():
        raise HouseCupException(deduct_error)
    amount = int(args[2])

    new_amount = participants[person_id][MOD_ADJUST] - amount
    participants[person_id][MOD_ADJUST] = new_amount

    house = participants[person_id]["house"]
    adjective = HOUSE_TO_ADJECTIVE[house]
    msg = "The Word of the Mods is thus: you have been naughty."\
        " " + str(amount) + " " \
        "points from " + house.capitalize() + " for" \
        " " + person_mention + "'s bad deeds."
    return msg


def points(user, message):
    text = message.content
    args = text.split()

    person_id = user.id
    person_mention = user.mention

    mentioned = get_mention_user(False, message.mentions)
    if mentioned:
        person_id = mentioned.id
        person_mention = mentioned.mention
    elif len(args) > 1:
        raise HouseCupException(
            "To look up another user's points, mention them.")
    msg = ""

    if person_id not in participants:
        raise HouseCupException(
            person_mention + " is not currently participating in the house cup. :sob:")

    person = participants[person_id]
    rounded_score = str(round(calculate_personal_score(person_id), 2))

    who_message = person_mention + "'s points are:"
    total_message = "__**Total:  " + rounded_score + "**__"
    daily_message = format_name(
        CATEGORY_TO_EMOJI[DAILY], DAILY) + str(person[DAILY])
    post_message = format_name(
        CATEGORY_TO_EMOJI[POST], POST) + str(person[POST])
    beta_message = format_name(
        CATEGORY_TO_EMOJI[BETA], BETA) + str(person[BETA])
    comment_message = format_name(
        CATEGORY_TO_EMOJI[COMMENT], COMMENT) + str(person[COMMENT])
    workshop_message = format_name(
        CATEGORY_TO_EMOJI[WORKSHOP], WORKSHOP) + str(person[WORKSHOP])
    excred_message = format_name(
        CATEGORY_TO_EMOJI[EXCRED], EXCRED) + str(person[EXCRED])
    wc_message = format_name(
        CATEGORY_TO_EMOJI[WC], WC) + str(person[WC]) + " " \
        "(%d words)" % person["word_count"]

    msg = "\n".join([who_message, total_message, daily_message, post_message,
                     beta_message, comment_message, workshop_message,
                     wc_message, excred_message])

    if person[MOD_ADJUST] != 0:
        msg = msg + "\n" + format_name(
            CATEGORY_TO_EMOJI[MOD_ADJUST],
            MOD_ADJUST) + str(person[MOD_ADJUST])

    return msg


def house_points(user, message):
    text = message.content
    args = text.split()
    house = get_house(user)
    msg = ""

    if len(args) > 1:
        possible_house = args[1].lower()
        if possible_house not in HOUSES:
            raise HouseCupException(
                possible_house + " is not a valid house. Try `" + PREFIX + "housepoints slytherin`")
        else:
            house = possible_house

    # Sort by total points
    members = get_paticipants(house)
    sorted_members = sort_participants(members, "total")

    house_total = round(calculate_house_score(house), 2)
    heart = HOUSE_TO_HEART[house] + " "
    house_title = heart + "__**" + house.capitalize() + ":** "
    msg = house_title + str(house_total) + "__ " + heart + "\n"

    # Add each member to return message
    for index, (member, total_points) in enumerate(sorted_members):
        formatted_name = format_name(index + 1, member["name"])
        msg = msg + formatted_name + str(total_points) + "\n"

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
    valid_args = "Valid arguments to `" + PREFIX + "leaderboard` are " \
                "`daily`, `post`, `beta`, `workshop`, `comment`, `wc` (points)" \
                ", `word_count`, `excred`, `mod_adjust`, and `total`"
    msg = ""

    if len(args) > 1:
        category = args[1].lower()
        if category not in CATEGORIES + ["total", "word_count"]:
            raise HouseCupException(valid_args)

    sorted_members = sort_participants(participants.values(), category)[:5]

    msg = "__**Top 5 People for " + category.capitalize() + " Points:**__\n"
    if category == "word_count":
        msg = "__**Top 5 People for Total Word Count:**__\n"

    # Add each member to return message
    rank = 0
    previous_points = -43423478
    for index, (member, points) in enumerate(sorted_members):
        if points != previous_points:
            rank = index
        heart = "  " + HOUSE_TO_HEART[member["house"]]
        formatted_name = format_name(rank + 1, member["name"])
        msg = msg + formatted_name + str(points) + heart + "\n"
        previous_points = points

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


def get_sorted_houses():
    house_and_score = []

    for house in HOUSES:
        score = calculate_house_score(house)
        house_and_score.append((house, score))

    return sorted(house_and_score, key=lambda tup: tup[1], reverse=True)


def standings():
    sorted_houses = get_sorted_houses()
    first_place_house, first_place_score = sorted_houses[0]
    heart = HOUSE_TO_HEART[first_place_house]
    animal = HOUSE_TO_EMOJI[first_place_house]

    msg = heart + " **__Current Standings__** " + heart + "\n"
    number = 1
    for house, score in sorted_houses:
        rounded_score = round(score, 2)
        formatted_house = format_name(number, house)
        msg = msg + formatted_house + str(rounded_score) + "\n"
        number += 1

    return msg + heart + animal * 7 + heart


def winnings(user, message):
    """
    End and restarts the House Cup Compeition.
    Display Winners
    """
    global participants
    if not participants:
        raise HouseCupException(
            "There can be no winners with no participants. :sob:")

    user_is_mod = is_mod(user, message.channel)

    # Only Stuffle and Red can end the house cup
    if user.id not in ["478970983089438760", "438450978690433024"]:
        raise HouseCupException(
            "Only Stuffle and Red can declare the winners "
            "and restart the House Cup.")

    # Get Month and error check date
    # TODO: Is this happening in UTC?
    now = datetime.date.today()
    contest_month = now.strftime("%B")
    new_month = now.strftime("%B")
    day = now.day
    _, days_in_month = monthrange(now.year, now.month)

    if day == "1":
        yesterday = now - datetime.timedelta(days=1)
        contest_month = yesterday.strftime("%B")
    elif day == days_in_month:
        tomorrow = now + datetime.timedelta(days=1)
        new_month = tomorrow.strftime("%B")
    print(now)
    """else:
        raise HouseCupException(
            "Winnings can only be used at the end of the compeition. "
            "Please try again on the last day of the month, or the first UTC.")"""

    house_and_score = []
    for house in HOUSES:
        score = calculate_house_score(house)
        house_and_score.append((house, score))

    sorted_houses = sorted(
        house_and_score, key=lambda tup: tup[1], reverse=True)
    first_place_house, first_place_score = sorted_houses[0]
    heart = HOUSE_TO_HEART[first_place_house]
    animal = HOUSE_TO_EMOJI[first_place_house]

    msg = heart + animal * 7 + heart + "\n" \
        "**The House Cup is over!!!**\n\nCongratulations to **%s**, " \
        "the winners of %s's House Cup! \n\n" \
        "__Final scores are:__\n" % (
            first_place_house.capitalize(), contest_month)

    # Show standings
    number = 1
    for house, score in sorted_houses:
        formatted_house = format_name(
            HOUSE_TO_EMOJI[house] + " " + str(number), house)
        rounded_score = round(score, 2)
        msg = msg + formatted_house + str(rounded_score) + "  "
        msg = msg + HOUSE_TO_HEART[house] + "\n"
        number += 1

    # Thank you for participating
    mentions = [participants[p]["mention"] for p in participants]
    all_mentions = ", ".join(mentions)
    msg += "\nThank you to everyone who participated in this month's " \
        "House Cup: %s\n\n ~ " % all_mentions

    msg2 = "\nExtra congratulations to these participants who " \
        "went the extra mile and were top in their points category.\n"

    # Show top in category
    cats = ["total", "word_count"] + CATEGORIES
    cats.remove(DAILY)
    for category in cats:
        sorted_participants = sort_participants(
            participants.values(), category)
        top_member, points = sorted_participants[0]
        top_member_mentions = []
        for member, p in sorted_participants:
            if p == points:
                top_member_mentions.append(member["mention"])
        top_string = ", ".join(top_member_mentions)
        category_name = category.capitalize()
        category_announcement = CATEGORY_TO_EMOJI[category] + " **" \
            "" + category_name + ":** "
        msg2 += category_announcement + top_string
        msg2 += "—" + str(points) + "  "
        msg2 += HOUSE_TO_HEART[top_member["house"]] + "\n"

    msg2 += "\nWe hope to see you again next month. You may now " \
        "`%sjoin` %s's House Cup. Good luck, friend.\n" % (PREFIX, new_month)
    msg2 += heart + animal * 7 + heart

    # Make backup and reset scores
    make_backup(contest_month + "_final")
    participants = {}
    save_participants()
    global CAN_JOIN
    CAN_JOIN = True

    return (msg, msg2)


def ping_everyone(user, message):
    user_is_mod = is_mod(user, message.channel)

    if not user_is_mod:
        raise HouseCupException(
            "Only mods can ping all participants of the House Cup.")

    mentions = [participants[p]["mention"] for p in participants]
    if user.mention in mentions:
        mentions.remove(user.mention)
    return "Hey listen! %s has something to say!\n%s" % (
        user.mention, ", ".join(mentions))


def migrate(user):
    # TODO: data backups first
    stuffle_id = "438450978690433024"
    if user.id != stuffle_id:
        raise HouseCupException(
            "Only stuffle can run migrations.")
        # Todo: don't do migrations in the bot.

    for p in participants:
        print(p)
        if not WC in participants:
            participants[p][WC] = 0
            participants[p]["word_count"] = 0
    print("Data has been succesfully migrated")
    print(participants)


def make_backup(when):
    with open("data_backup_" + str(when), 'w', encoding='utf-8') as f:
        f.write(str(participants))


@client.event
async def on_message(message):
    user = message.author
    mention = user.mention
    text = message.content.lower()
    msg = ""

    # Prevent the bot from replying to itself
    if user == client.user:
        return

    if client.user.mentioned_in(message) and message.mention_everyone is False:
        random_person = get_random_person(user)
        msg = at(text, mention, random_person)

    # Ignore all messages not directed at bot
    if not message.content.startswith(PREFIX) and msg == "":
        return

    text = text[1:]
    args = text.split(" ")
    if len(args) == 0:
        return
    command = args[0]

    sorted_houses_i = get_sorted_houses()
    first_place_house_i, first_place_score_i = sorted_houses_i[0]

    try:
        argumentless_commands = [
            "join", "daily", "post", "beta", "workshop", "standings",
            "exercise"]
        if command in argumentless_commands and len(args) > 1:
            raise HouseCupException(
                "`%s%s` does not take any arguments. See `%shelp %s` "
                "for more information." % (PREFIX, command, PREFIX, command))

        if text.startswith("help"):
            embed = help_command(message, PREFIX)
            await client.send_message(message.channel, embed=embed)
            return

        # Join and Leave
        elif text.startswith("join"):
            msg = join(user)
            save_participants()
        elif text.startswith("leave"):
            msg = leave(user, message)
        elif text.startswith("actuallyleave"):
            msg = actually_leave(user)
            save_participants()

        # Edit Points
        elif text.startswith("log"):
            # Todo: Remove and refactor log
            msg = "{0.author.mention}: " + log_score(text, user)
            save_participants()
        elif text.startswith("daily"):
            msg = "{0.author.mention}: " + log_score("log daily", user)
            save_participants()
        elif text.startswith("post"):
            msg = "{0.author.mention}: " + log_score("log post", user)
            save_participants()
        elif text.startswith("beta"):
            msg = "{0.author.mention}: " + log_score("log beta", user)
            save_participants()
        elif text.startswith("comment"):
            msg = "{0.author.mention}: " + log_score("log " + text, user)
            save_participants()
        elif text.startswith("workshop"):
            msg = "{0.author.mention}: " + log_score("log workshop", user)
            save_participants()
        elif text.startswith("exercise"):
            msg = "{0.author.mention}: " + log_score("log exercise", user)
        elif text.startswith("wc"):
            msg = "{0.author.mention}: " + log_score("log " + text, user)
            save_participants()
        elif text.startswith("excred"):
            msg = "{0.author.mention}: " + log_score(
                  "log " + text, user)
            save_participants()
        elif text.startswith("remove"):
            msg = "{0.author.mention}: " + remove_score(text, user)
            save_participants()

        # Point viewing commands
        elif text.startswith("points"):
            msg = points(user, message)
        elif text.startswith("housepoints"):
            msg = house_points(user, message)
        elif text.startswith("leaderboard"):
            msg = leader_board(user, message)
        elif text.startswith("standings"):
            msg = standings()

        # Mod only commands
        elif text.startswith("award"):
            msg = award(user, message)
            save_participants()
        elif text.startswith("deduct"):
            msg = deduct(user, message)
            save_participants()
        elif text.startswith("migrate"):
            msg = migrate(user)
            save_participants()
        elif text.startswith("pingeveryone"):
            msg = ping_everyone(user, message)
        elif text.startswith("winnings"):
            msg1, msg2 = winnings(user, message)
            await client.send_message(message.channel, msg1.format(message))
            await client.send_message(message.channel, msg2.format(message))

        # For fun commands
        elif text.startswith("dumbledore"):
            house = get_house(user)
            embed = dumbledore(house, mention)
            await client.send_message(message.channel, embed=embed)
            return
        elif text.startswith("snape"):
            house = get_house(user)
            embed = snape(house, mention)
            await client.send_message(message.channel, embed=embed)
            return
        elif text.startswith("hermione"):
            house = get_house(user)
            embed = hermione(house, mention)
            await client.send_message(message.channel, embed=embed)
            return
        elif text.startswith("ron"):
            house = get_house(user)
            msg = ron(house)
        elif text.startswith("mcgonagall"):
            house = get_house(user)
            embed = mcgonagall(house, mention)
            await client.send_message(message.channel, embed=embed)
            return
        elif text.startswith("sneak"):
            random_person = get_random_person(user)
            msg = sneak(mention, random_person)

    except HouseCupException as ex:
        msg = "{0.author.mention}: " + str(ex)
        print(user.name + ": " + str(ex))
    except Exception as ex:
        msg = "Oh no! Something went wrong and I couldn't complete your "\
              " command. I'm so sorry! :sob: Ping stuffle if you need " \
              "help."
        await client.send_message(message.channel, msg.format(message))
        raise(ex)

    if msg:
        await client.send_message(message.channel, msg.format(message))

    sorted_houses = get_sorted_houses()
    first_place_house, first_place_score = sorted_houses[0]
    if first_place_house != first_place_house_i:
        standing = standings()
        surpassed_msg = "%s has surpassed %s in the standings!\n%s" % (
            first_place_house.capitalize(),
            first_place_house_i.capitalize(),
            standing)
        await send_to_all_servers(surpassed_msg)


async def send_to_all_servers(msg):
    for server in client.servers:
        if server.id in SERVER_ID_TO_CHANNEL:
            channel = client.get_channel(SERVER_ID_TO_CHANNEL[server.id])
            if channel:
                await client.send_message(channel, msg.format(msg))


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
    await client.change_presence(game=discord.Game(name="~help"))

    # If there is a problem loading data, make a backup and go offline
    # because the bot is effectively broken.
    try:
        load_participants()
    except Exception as ex:
        now = datetime.datetime.now()
        print("Making backup at %s" % str(now))
        make_backup(str(now))
        # TODO: Use send_to_all_servers
        for server in client.servers:
            if server.id in SERVER_ID_TO_CHANNEL:
                channel = client.get_channel(SERVER_ID_TO_CHANNEL[server.id])
                if channel:
                    msg = "I have had a critical data failue! :sob: " \
                          "I'm going away to rest until <@438450978690433024>"\
                          " fixes me."
                    await client.send_message(channel, msg.format(msg))
        await client.logout()
        print("Logged Out")
        raise ex


async def test_announce():
    print("Running test_announce")
    # TODO: Use send_to_all_servers
    for server in client.servers:
            if server.id in SERVER_ID_TO_CHANNEL:
                channel = client.get_channel(SERVER_ID_TO_CHANNEL[server.id])
                if channel:
                    msg = "This is a scheduled test message. " \
                          "<@438450978690433024>, it worked!"
                    await client.send_message(channel, msg.format(msg))


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        test_announce,
        'date',
        run_date=datetime.datetime(
            2019, 4, 12, 18, 30, 5, 0, datetime.timezone.utc))
    scheduler.start()

    client.loop.create_task(list_recs())
    token = os.environ.get("DISCORD_BOT_SECRET")
    client.run(token)

# TODO: Use APScheduler to schedule events like winnings
# TODO: Custom emoji
