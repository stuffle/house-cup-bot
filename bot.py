# Work with Python 3.6
import discord
import asyncio
import ast
import os



SLYTHERIN = "slytherin"
RAVENCLAW = "ravenclaw"
GRYFFINDOR = "gryffindor"
HUFFLEPUFF = "hufflepuff"

DAILY = "daily"
POST = "post"
BETA = "beta"
WORKSHOP = "workshop"
COMMENT = "comment"
EXCRED = "excred"

client = discord.Client()
participants = {}



def load_participants():
    global participants

    with open("data.json", encoding='utf-8') as f:
        file_text = f.read()
        participants = ast.literal_eval(file_text)



def save_participants():
    with open("data.json",'w',encoding = 'utf-8') as f:
        f.write(str(participants))



def get_house(user):
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
            "You cannot enter the house cup with multiple house roles.")

    return house


def get_paticipants(house):
    members = []
    for p in participants:
        member = participants[p]
        if member["house"] == house:
            members.append(member)
    print("Mebers: of " + house + str(members))
    return members



def calculate_personal_score(user_id):
    p = participants[user_id]
    return p["daily"] + p["post"] + p["beta"] + p["workshop"] + p["comment"] + p["excred"]



def join(user):
    """
    TODO: Implement deadline for joining
    """
    if user.id in participants.keys():
        raise Exception("You have already joined the house cup for this month.")

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

    return "Welcome to the House Cup {0.author.mention}! May the odds be ever in " + house.capitalize() + "'s favor."



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
    valid_categories = "Valid arguments to `~log` are `daily`, `post`, `beta`, `workshop`, `comment`, and `excred`"

    # Check if valid inputs
    if len(args) < 2:
        raise Exception("Please provide a category to log your points in. " + valid_categories)

    category = args[1].lower()
    if category not in [DAILY, POST, BETA, WORKSHOP, COMMENT, EXCRED]:
        raise Exception("Unrecognized Category. " + valid_categories)

    # Add points where appropriate
    if category == DAILY:
        participants[user.id][DAILY] = participants[user.id][DAILY] + 5
        msg = "Congratulations on doing something today—take 5 points for " + house + "! :heart:"
    if category == POST:
        participants[user.id][POST] = participants[user.id][POST] + 10
        msg = "YESSS!!! :eyes: :eyes: 10 points to " + house + "!"
    if category == BETA:
        participants[user.id][BETA] = participants[user.id][BETA] + 10
        msg = "You're a better beta than Harry is an omega. :wink:\n10 points to " + house + "!"
    if category == WORKSHOP:
        participants[user.id][WORKSHOP] = participants[user.id][WORKSHOP] + 30
        msg = "Thank you for putting your work up for the weekly workshop ~~gangbang~~. Take a whopping 30 points for " + house + "!"
    if category == COMMENT:
        participants[user.id][COMMENT] = participants[user.id][COMMENT] + 5
        msg = "Comments are so appreciated. :sparkling_heart: 5 points to " + house + "!"
    if category == EXCRED:
        if len(args) <= 2:
            raise Exception("Please provide an amount for the extra credit, like `~log excred 10`")
        if not args[2].isdigit():
            raise Exception("Extra credit amount must be a number. Try something like `~log excred 10`")
        amount = int(args[2])
        new_excred_total = participants[user.id][EXCRED] + amount
        if new_excred_total >= 50:
            new_excred_total = 50
            msg = "Your extra credit score has been set to the maximum, 50. Thank you for contributing so much! :heart:"
        elif amount == 0:
            raise Exception("Please provide the amount of extra credit points earned. For example: `~log excred 20`")
        else:
            msg = str(amount) + " points to " + house + " for extra credit work!"
        participants[user.id][EXCRED] = new_excred_total

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
        raise Exception("You can only look up the points of one user at a time.")
    elif len(args) > 1 and len(message.mentions) == 0:
        raise Exception("In order to look up the points of someone else, you must mention them. For example: `~points @person`. Or, to look at your own score, use `~ponts`")

    if person_id not in participants:
        raise Exception(person_mention + " is not currently participating in the house cup. :sob:")

    person = participants[person_id]

    msg = person_mention + "'s points are:\n" \
          "```Total: " + str(calculate_personal_score(person_id)) + "\n\n" \
          "Daily: " + str(person["daily"]) + "\n" \
          "Post: " + str(person["post"]) + "\n" \
          "Beta: " + str(person["beta"]) + "\n" \
          "Workshop: " + str(person["workshop"]) + "\n" \
          "Comment: " + str(person["comment"]) + "\n" \
          "Extra Credit: " + str(person["excred"]) + "```"

    return msg



def dumbledore():
    """
    TODO: Replace with CHRain's code
    """
    embed = discord.Embed(
        description="yada yada ding dong",
        color=0x000000)
    embed.set_author(name="Dumbledore:")
    embed.set_thumbnail(
        url="https://media1.tenor.com/images/f59d48f20907d137a3c6aaba9ab31f7e/tenor.gif?itemid=3495399")
    return embed



@client.event
async def on_message(message):
    user = message.author
    text = message.content
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

        elif text.startswith("~log"):
            msg = "{0.author.mention}: " + log_score(text, user)
            save_participants()

        elif text.startswith("~points"):
            msg = points(user, message)

        elif text == "~dumbledore":
            embed = dumbledore()
            await client.send_message(message.channel, embed=embed)
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
