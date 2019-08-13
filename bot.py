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
import pickle

from humor_commands import *
from actions import *
from inspire import *
from help import *
from mod import *
from marriages import *
from constants import *
import marriages
import mod


IS_TEST_ENV = os.environ.get("IS_TEST_ENV")
PREFIX = "~"
if IS_TEST_ENV:
    PREFIX = "$"
DATA_FILE = "data.json"
if IS_TEST_ENV:
    DATA_FILE = "test_data.json"


VALID_CATEGORIES = "Valid arguments to this command are `daily`, `post`," \
                   " `art`, `beta`, `workshop`, `exercise`, `comment`, " \
                   "`wc`, and `excred`"

client = discord.Client(status="~help")
scheduler = AsyncIOScheduler()
participants = {}
CAN_JOIN = False


class HouseCupException(Exception):
    pass


def load_participants():
    global participants

    with open(DATA_FILE, 'rb') as f:
        data = pickle.load(f)
        participants = data["participants"]
        mod.voting = data["voting"]
        marriages.proposals = data["proposals"]
        marriages.marriage_info = data["marriage_info"]


def save_participants():
    with open(DATA_FILE, 'wb') as f:
        data = {
            "participants": participants,
            "voting": mod.voting,
            "proposals": marriages.proposals,
            "marriage_info": marriages.marriage_info
        }
        pickle.dump(data, f)


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
    return int(user_id)


def calculate_personal_score(user_id):
    p = participants[user_id]
    points = p[DAILY] + p[POST] + p[BETA] + p[WORKSHOP] + p[COMMENT]
    points += p[WC] + p[ART] + p[EXCRED] + p[MOD_ADJUST]
    return points


def format_name(number, name):
    formatted_number = "**" + str(number) + "** "
    formatted_name = "`" + name.capitalize() + "`: "
    return formatted_number + formatted_name


def join(user):
    if user.id in participants.keys():
        raise HouseCupException(
            "You have already joined the house cup for this month.")

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
        ART: 0,
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
    msg = "Are you sure you want to leave the House Cup? " \
          "You are **not** allowed to switch houses during the month.\n\n" \
          "If you leave, your score will be wiped out. " \
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


def log_score(text, user_id):
    """
    Record house points.

    Text example: `~log excred 20`
    """
    msg = ""
    args = text.split()
    amount = 0
    quotes = []

    if user_id not in participants:
        raise HouseCupException(
            "Please join the house cup with `" + PREFIX + "join`")

    house = participants[user_id]["house"].capitalize()
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

    if category not in [EXCRED, COMMENT, DAILY, WORKSHOP, WC, "exercise", "art"]:
        points = CATEGORY_TO_POINTS[category]
        participants[user_id][category] = participants[user_id][category] + points

    # Add points where appropriate
    if category == DAILY:
        msg = "Congratulations on doing something creatively productive " \
              "today—take 5 points for " + house + "! " + heart
        current_points = participants[user_id][DAILY] + 5
        today = datetime.date.today()
        _, days_in_month = monthrange(today.year, today.month)
        day = today.day
        if current_points > 5 * (day + 1) or current_points > 5 * days_in_month:
            raise HouseCupException(
                "This daily was not logged because then you would have "
                "more dailies than are possible on this date.")
        last_daily = 0
        if "last_daily" in participants[user_id].keys():
            last_daily = participants[user_id]["last_daily"]
        now = time.time()
        eight_hours = 14400 * 2  # seconds
        if last_daily + eight_hours > now:
            raise HouseCupException(
                "Please adhere to the rules of only using this "
                "command once per day and only for days that you have been "
                "creatively productive.")
        participants[user_id][DAILY] = current_points
        participants[user_id]["last_daily"] = now

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

    if category == "art":
        if len(args) <= 2:
            raise HouseCupException(
                "Please provide an amount for the art,"
                " like `" + PREFIX + "art 10`")
        if not args[2].isdigit():
            raise HouseCupException(
                "Art amount must be a number. Try something "
                "like `" + PREFIX + "art 10`")
        amount = int(args[2])
        new_art_total = participants[user_id][ART] + amount
        if amount not in [5, 10, 15, 20]:
            raise HouseCupException(
                "The amount of art points must be 5, 10, 15, or 20")
        else:
            msg = "%d points to %s! Thank you for sharing your creation. " \
                  ":art:" % (amount, house)
        participants[user_id][ART] = new_art_total

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
        participants[user_id][WORKSHOP] = participants[user_id][WORKSHOP] + 5

    if category == WORKSHOP:
        msg = "Thank you for putting your work up for the weekly workshop " \
              "~~gangbang~~. Take a whopping 30 points for " + house + "!"
        last_workshop = 0
        if "last_workshop" in participants[user_id].keys():
            last_workshop = participants[user_id]["last_workshop"]
        now = time.time()
        one_day = 86400  # seconds
        if last_workshop + one_day > now:
            raise HouseCupException(
                "You may only log a workshop once per day. "
                "You must wait 24 hours between logging workshops.")
        participants[user_id][WORKSHOP] = participants[user_id][WORKSHOP] + 30
        participants[user_id]["last_workshop"] = now

    if category == COMMENT:
        new_value = participants[user_id][COMMENT]
        if len(args) < 3:
            msg = "Comments are so appreciated. :revolving_hearts: 1 point to"\
                  " " + house + "!"
            new_value += 1
        elif args[2] in ["extra", "essay", "long", "mystery"]:
            msg = "You've probably made someone really happy with your long " \
                  "and thoughtful comment! Good job! :sparkling_heart: " \
                  "5 points to " + house + "!"
            new_value += 5
        else:
            raise HouseCupException(
                "Unrecognized argument to `%scomment`. For a regular comment, "
                "do `%scomment`. For an essay length comment, do "
                "`%scomment extra`" % (PREFIX, PREFIX, PREFIX))
        if new_value >= 200:
            new_value = 200
            msg = "Your comment total has been set to the max—200. Thank you " \
                "for commenting so much. Your efforts are very appreciated. %s" % heart
        participants[user_id][COMMENT] = new_value

    if category == WC:
        wordcount = 0
        wc_points = 0
        amount = 0
        if "word_count" in participants[user_id]:
            wordcount = participants[user_id]["word_count"]
        if WC in participants[user_id]:
            wc_points = participants[user_id][WC]
        old_word_count = wordcount
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
        participants[user_id]["word_count"] = wordcount
        if args[2] == "add":
            msg = "Congratulations on posting %d words! " \
                "This brings your total to %d, giving you %d point%s! " % (
                    amount, wordcount, wc_points, plural) + msg
        else:
            msg = "Your total wordcount went from %d to %d, giving you %d point%s! " \
                "Congratulations! " % (
                    old_word_count, wordcount, wc_points, plural) + msg
        participants[user_id][WC] = wc_points

    if category == EXCRED:
        if len(args) <= 2:
            raise HouseCupException(
                "Please provide an amount for the extra credit, like `" + PREFIX + "excred 10`")
        if not args[2].isdigit():
            raise HouseCupException(
                "Extra credit amount must be a number. Try something like `" + PREFIX + "excred 10`")
        amount = int(args[2])
        new_excred_total = participants[user_id][EXCRED] + amount
        if new_excred_total >= 50:
            new_excred_total = 50
            msg = "Your extra credit score has been set to the maximum, 50." \
                  " Thank you for contributing so much! :heart:"
        elif amount == 0:
            raise HouseCupException(
                "Please provide the amount of extra credit points earned. For example: `" + PREFIX + "excred 20`")
        else:
            msg = str(amount) + " points to " + house + " for extra credit work!"
        participants[user_id][EXCRED] = new_excred_total

    # If I still set msg, there is only one possible response
    if msg:
        return msg

    return random.choice(quotes)


def remove_score(text, user_id):
    msg = ""
    args = text.split()
    amount = 0

    if user_id not in participants:
        raise HouseCupException("You can't remove points because you're not in the house cup. :sob:")

    house = participants[user_id]["house"].capitalize()

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
        new_points = participants[user_id][EXCRED] - points
    elif category == ART:
        if len(args) <= 2:
            raise HouseCupException(
                "Please provide an amount for art, like "
                "`" + PREFIX + "remove art 10`")
        if not args[2].isdigit():
            raise HouseCupException(
                "Art amount must be a number. "
                "Try something like `" + PREFIX + "remove art 10`")
        amount = int(args[2])
        if amount not in [5, 10, 15, 20]:
            raise HouseCupException(
                "Please provide a valid amount of art points to "
                "remove. Amount can be 5, 10, 15, or 20")
        points = amount
        new_points = participants[user_id][ART] - points
    elif category == "exercise":
        points = 5
        new_points = participants[user_id][WORKSHOP] - 5
        category = WORKSHOP
    elif category == "comment" and len(args) > 2:
        if args[2] in ["extra", "essay", "mystery"]:
            points = 5
            new_points = participants[user_id][category] - points
        else:
            raise HouseCupException(
                "If you want to remove a regular comment, do "
                "`%sremove comment`. "
                "If you want to remove an 5 point comment, do "
                "`%sremove comment extra`." % (PREFIX, PREFIX))
    else:
        points = CATEGORY_TO_POINTS[category]
        new_points = participants[user_id][category] - points

    if new_points < 0:
        raise HouseCupException(
            "No points were taken from you because this would set your "
            "total in " + str(category).capitalize() + " to "
            "a negative number.")
    else:
        participants[user_id][category] = new_points
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
            "You can only use this command for one user at a time.")
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
    now = time.time()
    time_remaining = now - person["last_daily"]
    hours = time_remaining // 3600
    plural = ""
    if hours != 1:
        plural = "s"

    who_message = person_mention + "'s points are:"
    total_message = "__**Total:  " + rounded_score + "**__"
    daily_message = format_name(
        CATEGORY_TO_EMOJI[DAILY], DAILY) + str(
            person[DAILY])
    last_daily_message = "`Last Daily`: %s UTC (%d hour%s ago)" % (
        time.strftime("%a, %b %d at %H:%M", time.gmtime(person["last_daily"])),
        hours,
        plural)
    post_message = format_name(
        CATEGORY_TO_EMOJI[POST], POST) + str(person[POST])
    beta_message = format_name(
        CATEGORY_TO_EMOJI[BETA], BETA) + str(person[BETA])
    art_message = format_name(
        CATEGORY_TO_EMOJI[ART], ART) + str(person[ART])
    comment_message = format_name(
        CATEGORY_TO_EMOJI[COMMENT], COMMENT) + str(person[COMMENT])
    workshop_message = format_name(
        CATEGORY_TO_EMOJI[WORKSHOP], WORKSHOP) + str(person[WORKSHOP])
    excred_message = format_name(
        CATEGORY_TO_EMOJI[EXCRED], EXCRED) + str(person[EXCRED])
    wc_message = format_name(
        CATEGORY_TO_EMOJI[WC], WC) + str(person[WC]) + " " \
        "(%d words)" % person["word_count"]

    points_messages = [who_message, total_message, daily_message]
    if person["last_daily"] != 0:
        points_messages.append(last_daily_message)
    points_messages = points_messages + [
        post_message, beta_message, art_message,
        comment_message, workshop_message,
        wc_message, excred_message]
    msg = "\n".join(points_messages)

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


def leader_board(text):
    """
    Show top 5 students in a given category
    """
    args = text.split()
    category = "total"
    valid_args = "Valid arguments to `" + PREFIX + "leaderboard` are " \
                "`daily`, `post`, `beta`, `art`, `workshop`, `comment`, `wc` (points)" \
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
    capped_points = []
    for points in sorted_points:
        if points >= 500:
            capped_points.append(500)
        else:
            capped_points.append(points)

    for index, points in enumerate(capped_points):
        iteration = index + 1
        weight = 1
        if iteration in [1, 2, 3]:
            weight = 1 / 4
        else:
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


def announce_two_days():
    current_standings = standings()
    msg = "There are exactly two days remaining in this month's House Cup. " \
          "Get your points in soon to help your house win. " \
          "Good luck friends." \
          "\n\n%s" % current_standings
    return msg


def winnings():
    """
    End and restarts the House Cup Compeition.
    Display Winners
    """
    global participants
    if not participants:
        raise HouseCupException(
            "There can be no winners with no participants. :sob:")

    # Get Month and error check date
    now = datetime.datetime.now(datetime.timezone.utc)
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

    msg += "\nExtra congratulations to these participants who " \
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
        msg += category_announcement + top_string
        msg += "—" + str(points) + "  "
        msg += HOUSE_TO_HEART[top_member["house"]] + "\n"

    msg += "\n~"

    # Thank you for participating
    mentions = [participants[p]["mention"] for p in participants]
    all_mentions = ", ".join(mentions)
    msg2 = "\nThank you to everyone who participated in this month's " \
        "House Cup: %s\n\n ~ " % all_mentions

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


def make_backup(when):
    with open("data_backup_" + str(when), 'w', encoding='utf-8') as f:
        f.write(str(participants))


def time_left():
    now = datetime.datetime.now(datetime.timezone.utc)
    winnings_date = datetime.datetime(
        now.year, now.month, days_in_month,
        23, 59, 0, 0, datetime.timezone.utc)

    time_remaining = winnings_date - now
    days = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds // 60) % 60

    msg = "There are %d days, %d hours, and %d minutes " \
          "remaining." \
          " Good luck, friend." % (days, hours, minutes)
    return msg


# {competitor1_mention: {better_mention: 5}}
bets = {}


async def wrestle(hugger, message):
    """Inspiration from RedHorse and other beta readers"""
    global bets

    if bets:
        return "%s: Sorry, but only one wrestling match can occur at a time." % hugger

    participants = [hugger]
    mentions = message.mentions
    challenger = ""
    fluids = [
        "mud",
        "jelly",
        "icing",
        "blood",
        "melted chocolate",
        "soap",
        "chili"
    ]
    fluid = random.choice(fluids)

    if len(mentions) == 1:
        challenger = mentions[0].mention
        participants.append(challenger)
        if challenger == "<@542048148776943657>":
            rs = [
                "%s steps into a pool filled with %s. %s looks at stufflebot expectantly. stufflebot blinks. The pool disappears, and %s is suddenly sprawled on the ground.\n\nDo not try to wrestle stufflebot. You will always lose." % (
                    hugger, fluid, hugger, hugger),
                "%s wakes up in a pool full of %s with no idea of how they got there. stufflebot stands emotionlessly over them with a trophy in hand. %s is missing 10 points." % (
                    hugger, fluid, hugger),
                "%s stares at stufflebot over the edge of the pool filled with %s. stufflebot stares back, its robot face fixed in an unchanging, cute smile. Feeling uneasy, %s steps into the rink. stufflebot takes a step forward. The reflection in its eye that was once so adorable now seems menacing. %s shakes it off and prepares to fight. stufflebot steps into the rink. As soon as the start of the match is called, an electric pulse radiates through the %s, and %s falls to the ground, convulsing." % (
                    hugger, fluid, hugger, hugger, fluid, hugger),
                "stufflebot shows up to the wrestling match alone. No one knows where %s is. stufflebot is declared the victor." % (
                    hugger)
            ]
            return random.choice(rs)
        if challenger == hugger:
            return "%s steps into an empty pool by themself. %s raises a hand and slaps their own face.\n\nWhen you wrestle with yourself, there is no winning. Only lonely defeat." % (hugger, hugger)
    else:
        return "Please mention one user to wrestle them."

    bets = {
        hugger: {},
        challenger: {}
    }

    scheduler.add_job(
        func=finish_wrestling,
        trigger='interval',
        minutes=1,
        args=[message, participants, fluid],
        id='001')

    return "Taking bets on %s VS %s! The match begins in 60 seconds!\n\n" \
        "Bets are for **real** house points. You may bet up to 5 points. " \
        "To bet, type `~bet @person 5`" % (
        hugger, challenger)


def bet(person, mentions, text):
    person_id = get_userid_from_mention(person)
    if person_id not in participants.keys():
        raise HouseCupException(
            "You must `~join` the House Cup in order to bet.")

    args = text.split(" ")
    if len(mentions) == 0:
        raise(HouseCupException("You must mention a user to bet on them."))
    if len(mentions) > 1:
        raise(HouseCupException("You may only bet on one user at a time."))
    bettee = mentions[0].mention

    if len(args) != 3:
        raise(HouseCupException(
            "Correct betting format is `~bet @person amount`. Please try again."
        ))
    if not args[2].isdigit():
            raise HouseCupException(
                "You must bet an amount between 0 and 5. "
                "Valid format: `~bet @person 5`")
    amount = int(args[2])
    if amount > 5 or amount < 0:
        raise HouseCupException("You must bet an amount between 0 and 5.")

    if bettee not in bets.keys():
        raise HouseCupException(
            "%s is not currently participating in a wrestling match." % bettee)

    bets[bettee][person] = amount
    return "%s: You have bet %d real house points on %s." % (
        person, amount, bettee)


async def finish_wrestling(message, members, fluid):
    global bets
    global participants

    scheduler.remove_job('001')
    winner = random.choice(members)
    members.remove(winner)
    loser = members[0]

    responses = [
        "%s slips while stepping into the rink, making an easy victory for %s." % (
            winner, loser),
        "As soon as the match begins, %s tackles %s. They fall to the ground landing in the %s. They struggle for control until %s manages to flip them over, pinning %s and winning the match." % (
            loser, winner, fluid, winner, loser),
        "They size each other up for several moments before %s steps forward, slipping in the %s. Mid fall they reach out, grabbing %s and managing to bring them down too. %s is dazed, and %s takes the win." % (
            winner, fluid, loser, loser, winner),
        "%s manages to grasp the legs of %s, lifting them overhead and throwing them into the %s. %s is dazed, and %s takes the win." % (
            winner, loser, fluid, loser, winner),
        "They flail feebly at each other as if fighting off invisible bees. %s is out of breath first, allowing %s to subdue them." % (
            loser, winner),
        "%s does an impressive throwdown, making %s drink a mouthful of %s. %s splutters feebily for a moment before they tap out, losing the match." % (
            winner, loser, fluid, loser),
        "The battle, if you want to call it that, is short-lived. %s always said they weren’t the outdoorsy type. It's an easy victory for %s." % (
            loser, winner),
        "After a tense staredown, %s uses bubble beam! The ref calls foul on %s for the illegal use of Pokémon moves." % (
            loser, loser),
        "%s stubs a toe and falls into %s. The fight was over before it began. %s shakes their head not quite believing it as they are declared the winner so quickly." % (
            loser, winner, winner),
        "%s tries to use the killing curse. The ref, aghast that a death eater has snuck into the match, ends it quickly. The ref needn't have worried—%s has never been able to cast the curse successfully. Harry smirked from the side-lines, pointing at his scar." % (
            loser, loser),
        "%s distracts %s with NSFW Tomarry pictures and does a successful tackle. The pictures land into the %s and the crowd storm the rings, eager for a better look! %s is trampled into the %s." % (
            loser, winner, fluid, loser, fluid),
        "%s and %s face each other across the %s. Neither wants to end up in the %s. %s offers %s a cup of tea, and suggest they settle their differences like reasonable people. %s agrees and, after a lengthy discussion, they come to a mutually beneficial arrangement. According to their agreement, %s wins!" % (
            winner, loser, fluid, fluid, winner, loser, loser, winner)
    ]

    commentary = random.choice(responses)
    msg = "%s and %s step into a large pool filled with %s. %s\n\n**%s WINS**\n" % (
        winner, loser, fluid, commentary, winner
    )

    # Settle Bets
    results = []
    for person in bets[winner]:
        amount = bets[winner][person]
        p_id = get_userid_from_mention(person)
        house = participants[p_id]["house"].capitalize()
        participants[p_id][MOD_ADJUST] = participants[p_id][MOD_ADJUST] + amount
        total_points = calculate_personal_score(p_id)
        win_msg = "%s: You have **won** %d points for %s! " \
            "This brings your total points to %d!" % (
                person, amount, house, total_points)
        results.append(win_msg)

    for person in bets[loser]:
        amount = bets[loser][person]
        p_id = get_userid_from_mention(person)
        house = participants[p_id]["house"].capitalize()
        participants[p_id][MOD_ADJUST] = participants[p_id][MOD_ADJUST] - amount
        total_points = calculate_personal_score(p_id)
        lose_msg = "%s: You have **lost** %d points for %s! " \
            "This brings your total points to %d!" % (
                person, amount, house, total_points)
        results.append(lose_msg)

    for m in results:
        msg = msg + "\n%s" % m

    bets = {}
    await message.channel.send(msg.format(message))


@client.event
async def on_raw_reaction_add(payload):
    await check_reactions(payload, client)


@client.event
async def on_message(message):
    channel = message.channel
    user = message.author
    user_id = user.id
    mention = user.mention
    text = message.content.lower()
    msg = ""

    # Prevent the bot from replying to itself
    if user == client.user:
        return

    sorted_houses_i = get_sorted_houses()
    first_place_house_i, first_place_score_i = sorted_houses_i[0]

    try:
        # msg will be overwritten if @stufflebot is an argument to another command
        if client.user.mentioned_in(message) and message.mention_everyone is False:
            random_person = get_random_person(user)
            if "i love you" in text:
                msg = "%s: %s" % (mention, i_love_you(random_person))
            else:
                msg = at(text, mention, random_person)

        if message.channel.type.name in ["private", "group"]:
            raise HouseCupException(
                "Please communicate with in a server we share.")

        # Add bananalion to everything wolven says in the writing server
        if user.id == 593530774104309790 and message.guild.id == 497039992401428498:
            banana_lion = client.get_emoji(564830356977483804)
            await message.add_reaction(banana_lion)
        # Add banana badger to everything Ava says in the writing server
        if user.id == 516122981156782091 and message.guild.id == 497039992401428498:
            banana_bad = client.get_emoji(565106770020925451)
            await message.add_reaction(banana_bad)

        modded = mod_message(text, mention, message.channel.id)
        if modded:
            await channel.send(modded.format(message))
            return

        # Ignore all messages not directed at bot unless it was a mention
        if not message.content.startswith(PREFIX) and msg == "":
            return

        text = text[1:]
        args = text.split(" ")
        if len(args) == 0:
            return
        command = args[0]

        argumentless_commands = [
            "join", "daily", "post", "beta", "workshop", "standings",
            "exercise"]
        if command in argumentless_commands and len(args) > 1:
            raise HouseCupException(
                "`%s%s` does not take any arguments. See `%shelp %s` "
                "for more information." % (PREFIX, command, PREFIX, command))

        if text.startswith("help"):
            embed = help_command(message, PREFIX)
            await channel.send(embed=embed)
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
            msg = "{0.author.mention}: " + log_score(text, user_id)
            save_participants()
        elif text.startswith("daily"):
            msg = "{0.author.mention}: " + log_score("log daily", user_id)
            save_participants()
        elif text.startswith("post"):
            msg = "{0.author.mention}: " + log_score("log post", user_id)
            save_participants()
        elif text.startswith("art"):
            msg = "{0.author.mention}: " + log_score("log " + text, user_id)
            save_participants()
        elif text.startswith("beta"):
            msg = "{0.author.mention}: " + log_score("log beta", user_id)
            save_participants()
        elif text.startswith("comment"):
            msg = "{0.author.mention}: " + log_score("log " + text, user_id)
            save_participants()
        elif text.startswith("workshop"):
            msg = "{0.author.mention}: " + log_score("log workshop", user_id)
            save_participants()
        elif text.startswith("exercise"):
            msg = "{0.author.mention}: " + log_score("log exercise", user_id)
        elif text.startswith("wc"):
            msg = "{0.author.mention}: " + log_score("log " + text, user_id)
            save_participants()
        elif text.startswith("excred"):
            msg = "{0.author.mention}: " + log_score(
                  "log " + text, user_id)
            save_participants()
        elif text.startswith("remove"):
            msg = "{0.author.mention}: " + remove_score(text, user_id)
            save_participants()

        # Point viewing commands
        elif text.startswith("points"):
            msg = points(user, message)
        elif text.startswith("housepoints"):
            msg = house_points(user, message)
        elif text.startswith("leaderboard"):
            msg = leader_board(text)
        elif text.startswith("standings"):
            msg = standings()

        # Mod only commands
        elif text.startswith("echo"):
            if user.id != STUFFLE_ID:
                raise HouseCupException("Only stuffle can use echo.")
            msg = " ".join(text.split(" ")[1:])
        elif text.startswith("award"):
            msg = award(user, message)
            save_participants()
        elif text.startswith("deduct"):
            msg = deduct(user, message)
            save_participants()
        elif text.startswith("pingeveryone"):
            msg = ping_everyone(user, message)
        elif text.startswith("winnings"):
            if user.id not in [478970983089438760, 438450978690433024]:
                raise HouseCupException(
                    "Only Stuffle and Red can declare the winners "
                    "and restart the House Cup.")
            msg1, msg2 = winnings()
            print(msg1)
            await channel.send(msg1.format(message))
            await channel.send(msg2.format(message))
        elif text.startswith("startmonitoring"):
            user_is_mod = is_mod(user, message.channel)
            msg = await monitor_voting(text, is_mod, client)
            save_participants()
        elif text.startswith("stopmonitoring"):
            user_is_mod = is_mod(user, message.channel)
            msg = stop_monitor_voting(text, is_mod)
            save_participants()
        elif text.startswith("showmonitoring"):
            user_is_mod = is_mod(user, message.channel)
            msg = show_monitors(text, is_mod)
        elif text.startswith("pickwinner"):
            msg = await pick_winner(text, client)
        elif text.startswith("unwelcome"):
            msg = await unwelcome(client)
        elif text.startswith("clearchannels"):
            msg = await clear_channels(client, message)
        elif text.startswith("deletehistory"):
            msg = await delete_history(client, message)
        elif text.startswith("clearchannelnow"):
            msg = await clear_channel_now(client, message)
        elif text.startswith("captionshame"):
            msg = await captionshame(text, client)
        elif text.startswith("caption"):
            msg = await caption(text, client)

        # Marriage commands
        elif text.startswith("marry"):
            msg = marry(client, message)
            save_participants()
        elif text.startswith("divorce"):
            msg = divorce(client, message)
            save_participants()
        elif text.startswith("marriages"):
            msg = await see_marriages(client, message)
        elif text.startswith("testem"):
            msg = test_em(client, text)
        elif text.startswith("bless"):
            msg = bless(client, message)
            save_participants()

        # For fun commands
        elif text.startswith("dumbledore"):
            house = get_house(user)
            embed = dumbledore(house, mention)
            await channel.send(embed=embed)
            return
        elif text.startswith("snape"):
            house = get_house(user)
            embed = snape(house, mention)
            await channel.send(embed=embed)
            return
        elif text.startswith("hermione"):
            house = get_house(user)
            embed = hermione(house, mention)
            await channel.send(embed=embed)
            return
        elif text.startswith("ron"):
            house = get_house(user)
            msg = ron(house)
        elif text.startswith("harry"):
            msg = harry()
        elif text.startswith("mcgonagall"):
            house = get_house(user)
            embed = mcgonagall(house, mention)
            await channel.send(embed=embed)
            return
        elif text.startswith("sneak"):
            random_person = get_random_person(user)
            msg = sneak(mention, random_person)
        elif text.startswith("grouphug"):
            embed = group_hug(user.mention, message.mentions, text)
            await channel.send(embed=embed)
            return
        elif text.startswith("hug"):
            embed = hug(user.mention, message.mentions, text)
            await channel.send(embed=embed)
            return
        elif text.startswith("cheer"):
            embed = cheer(user.mention, message.mentions, text)
            await channel.send(embed=embed)
            return
        elif text.startswith("kidnap"):
            embed = kidnap(user.mention, message.mentions, text)
            await channel.send(embed=embed)
            return
        elif text.startswith("wrestle"):
            msg = await wrestle(mention, message)
        elif text.startswith("bet"):
            msg = bet(user.mention, message.mentions, text)
        elif text.startswith("pillage"):
            embed = pillage(user.mention)
            await channel.send(embed=embed)
            return
        elif text.startswith("madness"):
            embed = madness(user.mention, message.mentions)
            await channel.send(embed=embed)
            return
        elif text.startswith("shouldikillharry"):
            msg = "%s: %s" % (mention, should_i_kill())
        elif text.startswith("shouldigetbacktowork"):
            msg = "%s: %s" % (mention, back_to_work())
        elif text.startswith("randompair"):
            msg = "%s: %s" % (mention, random_pair())
        elif text.startswith("kink"):
            msg = "%s: %s" % (mention, kink())
        elif text.startswith("whenshouldtheyfuck"):
            msg = "%s: %s" % (mention, when_should_they_fuck())
        elif text.startswith("inspireme"):
            msg = "%s: %s" % (mention, inspireme())
        elif text.startswith("prompt"):
            random_person = get_random_person(user)
            msg = "%s: %s" % (mention, gen_prompt(mention, random_person))
        elif text.startswith("time"):
            msg = "%s: %s" % (mention, time_left())
        elif text.startswith("iloveyou"):
            random_person = get_random_person(user)
            msg = "%s: %s" % (mention, i_love_you(random_person))

    except (HouseCupException, mod.HouseCupException, MarriageException) as ex:
        msg = "{0.author.mention}: " + str(ex)
        print(user.name + ": " + str(ex))
    except Exception as ex:
        msg = "Oh no! Something went wrong and I couldn't complete your "\
              " command. I'm so sorry! :sob: Ping stuffle if you need " \
              "help."
        await channel.send(msg.format(message))
        raise(ex)

    if msg:
        await channel.send(msg.format(message))

    sorted_houses = get_sorted_houses()
    first_place_house, first_place_score = sorted_houses[0]
    if first_place_house != first_place_house_i:
        standing = standings()
        surpassed_msg = "%s has surpassed %s in the standings!\n%s" % (
            first_place_house.capitalize(),
            first_place_house_i.capitalize(),
            standing)
        await send_to_all_servers(surpassed_msg, SERVER_ID_TO_CHANNEL)


async def send_to_all_servers(msg, server_dict):
    for server in client.guilds:
        if server.id in server_dict:
            channel = client.get_channel(server_dict[server.id])
            if channel:
                await channel.send(msg.format(msg))


async def list_recs():
    await client.wait_until_ready()
    print("Current servers:")
    for server in client.guilds:
        print(server.name)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def run_winnings():
    print("running winnings")
    msg1, msg2 = winnings()
    print("winnings ran")
    await send_to_all_servers(msg1.format(msg1), SERVER_ID_TO_CHANNEL_ANNOUNCE)
    await send_to_all_servers(msg2.format(msg2), SERVER_ID_TO_CHANNEL_ANNOUNCE)


async def run_announce_two_days():
    print("Running announce_two_days")
    msg = announce_two_days()
    await send_to_all_servers(msg.format(msg), SERVER_ID_TO_CHANNEL_ANNOUNCE)


if __name__ == '__main__':
    client.loop.create_task(list_recs())
    token = os.environ.get("DISCORD_BOT_SECRET")

    # If there is a problem loading data, make a backup and abort start up
    try:
        load_participants()
    except Exception as ex:
        now = datetime.datetime.now(datetime.timezone.utc)
        print("Making backup at %s" % str(now))
        make_backup(str(now))
        raise ex

    now = datetime.datetime.now(datetime.timezone.utc)
    _, days_in_month = monthrange(now.year, now.month)

    # Schedule Events
    winnings_date = datetime.datetime(
        now.year, now.month, days_in_month,
        23, 59, 0, 0, datetime.timezone.utc)
    print(winnings_date)
    scheduler.add_job(
        run_winnings,
        'date',
        run_date=winnings_date)

    two_days_left = datetime.datetime(
        now.year, now.month, days_in_month - 2,
        23, 59, 0, 0, datetime.timezone.utc)
    print("Two days left: %s" % two_days_left)
    scheduler.add_job(
        run_announce_two_days,
        'date',
        run_date=two_days_left)

    scheduler.add_job(
        func=clear_channels,
        trigger='cron',
        day="*",
        hour="21",
        timezone="utc",
        args=[client])
    scheduler.add_job(
        func=unwelcome,
        trigger='cron',
        day="*",
        hour="22",
        timezone="utc",
        args=[client])

    scheduler.start()
    client.run(token)

# TODO: Custom emoji
