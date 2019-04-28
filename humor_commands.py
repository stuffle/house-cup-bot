import discord
import random


def get_random_embed(quote_dict, author, colour):
    quote, tup = random.sample(quote_dict.items(), 1)[0]
    gif, caption = tup

    embed = discord.Embed(
        color=colour,
        description=quote)
    embed.set_author(name=author + ":")
    embed.set_image(url=gif)
    embed.set_footer(text="Gif Caption: " + caption)
    return embed


def should_i_kill():
    responses = ["No."] * 8
    responses.append("Do what needs to be done.")
    responses.append("Why must you always do this? :weary:")
    responses.append("Yes. \"Sometimes the plot demands a death.\"—Earth")
    return random.choice(responses)


def gen_prompt(mention, ran_person):
    person = [
        "Harry",
        "Ron",
        "Hermione",
        "Voldemort",
        "Tom",
        "Dumbledore",
        "Snape",
        "Umbridge",
        "Ginny",
        "Draco",
        "Tom Riddle Sr.",
        "The Golden Trio",
        "The Locket Horcrux",
        "The Diary Horcrux",
        "The Scar Horcrux",
        "The Cup Horcrux",
        "The Diadem Horcrux",
        "Nagini",
        "Sixty-year-old Harry Potter",
        "Sirius",
        "Remus",
        "Fluffy, the Cerberus",
        "Dobby, the house-elf",
        "Norberta, the Norwegian Ridgeback Dragon",
        "Merope",
        "Grindelwald",
        "Your OT3",
        mention,
        mention,
        ran_person,
        ran_person
    ]
    random_person = random.choice(person)

    action = [
        "should not have ventured into",
        "inherits",
        "has to sit for NEWTs at",
        "is caught smoking weed in",
        "sets fire to",
        "opens a Magical Creatures shelter at",
        "locks themself into",
        "regrets the day they first saw",
        "hides their most prized possession in",
        "reflects on it all at",
        "finds a new favorite makeout spot in",
        "wakes up still drunk in",
        "finds a baby in a basket at",
        "brought the war to",
        "takes the Dark Mark at",
        "gets married in",
        "encountered the Mirror of Erised in",
        "loves to have tea at",
        "discovers a new kink in",
        "seduces an enemy at",
        "plans a fancy dress party at",
        "redecorates",
        "does a ritual at",
        "cries in",
        "opens a center for homeless garden gnomes at",
        "meets a mysterious Squib in",
        "meets a solicitor in secret at",
        "never intended to return to",
        "discovers a creature inheritance at",
        "plots world domination from",
        "climbs on to come at",
        "cackles like a loon at",
        "runs away from a Nundu in",
        "likes to boogie down at",
        "held a protest at",
        "wakes up with no memory of how they got there at",
        "Apparates with ill-intentions to",
        "commits their first murder at"
    ]
    random_action = random.choice(action)

    setting = [
        "Hogwarts Castle",
        "12 Grimmauld Place",
        "the Ministry of Magic",
        "a mysterious Muggle residence",
        "the Little Hangleton Graveyard",
        "a beachside cave",
        "the Forbidden Forest",
        "an office building",
        "the Muggle parliament",
        "the Room of Requirement",
        "the Chamber of Secrets",
        "their childhood bedroom",
        "Dumbledore’s office",
        "the Quidditch pitch",
        "the residence of the Supreme Mugwump",
        "the Black Lake",
        "Number Four Privet Drive",
        "the back garden of the Burrow",
        "King’s Cross Station",
        "Platform 9 ¾",
        "Wool’s Orphanage",
        "the top of Mount Everest",
        "the Albanian Forest",
        "the Sahara Desert",
        "Madam Puddifoot’s",
        "Nurmengard"
    ]
    random_setting = random.choice(setting)

    return "%s %s %s." % (random_person, random_action, random_setting)


def dumbledore(house, mention):
    """
    Written by CHRain
    """
    house = house.capitalize()

    quotes = {
        "I’m afraid after I take points from you, the likely result will be death caused by angry housemates, but do not fret. After all, to the well-organized mind, death is but the next great adventure. Good Luck, " + mention + ". 50 points from " + house + "!" : (
            " https://media.giphy.com/media/720g7C1jz13wI/giphy.gif ",
            "Dumbledore, in dignified blue robes and hat, is so disappointed in you that he throws up his arms and rolls his eyes."),
        "Do you feel pain, " + mention + "? Pain from losing house points, yet again? Remember, the fact that you can feel pain like this is your greatest strength. 50 points from " + house + "." : (
            " https://media.giphy.com/media/xqn7gb9F4tl2U/giphy.gif ",
            "Dumbledore, colored in black and white that truly show his age, shakes his head sagely as he utters, \"It is our choices that show what we truly are.\""),
        "20 points from " + house + "! Anguish. It’s an emotion all of us must face at one point in our lives, I’m afraid. As a man who has lived that life, I give you wisdom: we must try not to sink beneath our anguish, but battle on. " : (
            " https://media.giphy.com/media/14q7kvYacWa2I0/giphy.gif ",
            "Dumbledore, looking weary and bedraggled, and wearing white robes (because this is from that scene in which they're dead) glances upwards, as if remembering the memories of the past."),
        "Your act of kindness warms my heart and soothes my soul. Thank you, " + mention + ", for typing the dumbledore command. It's lucky it's dark. I haven't blushed so much since Madam Pomfrey told me she liked my new earmuffs. 10 points to " + house + "." : (
            " https://media.giphy.com/media/AOrThUuuOoDCg/giphy.gif ",
            "Dumbledore, sitting stoically on his throne above you,  pats his right hand in what we might assume, is his version of clapping for people like you. But, he makes an effort with the flashing caption: \"# DUMBLEDORE IS PLEASED\"."),
        "30 points to " + house +  "! Congratulations, " + mention + ". Off you trot, I am sure your " + house + " housemates are waiting to celebrate with you, and it would be a shame to deprive them of this excellent excuse to make a great deal of mess and noise. " : (
            " https://media.giphy.com/media/OU1marLMNNtnO/giphy.gif ",
            "Dumbledore, who is doing the chicken dance, stands next to an actually smiling Snape, with the caption \"PARTY HARD.\"")
    }

    return get_random_embed(quotes, "Dumbledore", 9110292)


def snape(house, mention):
    """
    Written by CHRain
    """
    house = house.capitalize()
    snape_dict = {
        "You’re a fool for typing this command. You’re just like the rest of the dunderheads that I have to face on a daily basis, always nattering and giggling like gossips. Wha—stop looking at me like that! 10 points from " + house + "! for looking at your professor rudely!" : (
            "https://media.giphy.com/media/4jXIVkgjhIQbS/giphy.gif",
            "Snape's dark eyes bore into you, growing larger until the only thing you see and know is his disapproval...and you know it's deserved."),
        "I heard from a little birdie that you have been slacking lately...silence! Whatever it is you want to say, I don’t want to hear it. There is no point in apportioning blame. What is done, is done. 10 points from " + house + "! For...disappointing your professor." : (
            "https://media.giphy.com/media/UAJpANY0bGPhS/giphy.gif",
            "Congratulations, you've managed to be such a bother that Snape is no longer stoic. His face crumples in agony as he orders \"SILENCE!\""),
        "10 points from " + house + "! I told you to not type this command. I do not take cheek from anyone...not even from ‘The Great " + mention + ".’" : (
            "https://media.giphy.com/media/ZIopqe1msuIFi/giphy.gif",
            "Snape, blending into the darkness, except the shine of his greasy hair and the reflection of his sallow face, slowly approaches you, with such a look that even you know not to test him."),
        "Your work as of late has suspiciously improved and while I have my suspicions as to why this happened, it would be remiss of me to not award your efforts, false or not. 10 points to " + house + ". ...do not think that my doubts have been eased " + mention + ", I’m watching you." : (
            "https://media.giphy.com/media/13gxK9D2PkTVgk/giphy.gif",
            "Snape, tilts his head towards you, as if to ask if you know what he means, but he knows that you don't.")
    }

    return get_random_embed(snape_dict, "Severus Snape", 4289797)


def sneak(mention, random_person):
    """
    Quotes written by Eath_Phoenix

    Todo Idea: Display sneak points in ~points
    """
    quotes = [
        "Hello %s I see you’re working hard to earn house points! However, I think %s needs more help than you do. 10 points to them." % (mention, random_person),
        "Thank you for your gallant efforts in earning house points %s, I think it only fair that %s takes them in your stead." % (mention, random_person),
        "Hm, this is tricky, I’m tempted to give %s your points, but I’ll let you keep them instead. This time." % random_person,
        "Brave are those who earn house points %s, braver still are those who take them form you. 10 points to %s!" % (mention, random_person),
        "10 points to %s, no, wait, that doesn’t sound right. 10 points to %s!" % (mention, random_person),
        "50 points to %s, and let this be a lesson to you, %s" % (random_person, mention)
        ]
    return random.choice(quotes)


def hermione(house, mention):
    """
    Quotes written by Batsutousai
    """

    house = house.capitalize()
    quotes = {
    "You've done something stupid, but somehow managed not to get caught by a professor or prefect. Impressive, " + mention + ". You neither gain nor lose points." : (
        "https://cdn.discordapp.com/attachments/562148502944350229/562387688645328940/expelled-Hermione.gif",
        "Hermione, looking back over her shoulder with the text \"We could have been killed, or worse, expelled\"."),
    "You've learnt how to cast a new spell! Congratulations, " + mention + "! 10 points to " + house + "!" : (
        "https://cdn.discordapp.com/attachments/562148502944350229/562387890089361443/leviosa-Hermione.gif",
        "Hermione, saying, \"It's LeviOsa, not LeviosA\", with the o capitalised in the first one, and the a capitalised in the second."),
    "You've managed to keep your friend from getting into a fight in view of a professor. 10 points to " + house + ". " : (
        "https://cdn.discordapp.com/attachments/562148502944350229/562388041050750997/makingaface-Hermione.gif",
        "Hermione pulling Harry away and making a disgusted face at the viewer."),
    "50 points to " + house + " for learning how to successfully cast the patronus charm!" : (
        "https://cdn.discordapp.com/attachments/562148502944350229/562388559340765184/patronus-Hermione.gif",
        "Hermione standing in the Room of Requirement, smiling as she twists to watch as her otter patronus jumps in a circle around her."),
    "20 points from " + house + " for punching a fellow student! Even if they did deserve it." : (
        "https://cdn.discordapp.com/attachments/562148502944350229/562388967132102669/punchDraco-Hermione.gif",
        "Hermione starts to turn away from Draco, who looks delighted, before turning back around to punch him in the face."),
    "10 points for always being ready with the answer, even when your classmates are being IDIOTIC CHILDREN." : (
        "https://cdn.discordapp.com/attachments/562148502944350229/562389131485904966/raisehand-Hermione.gif",
        "Hermione raises her hand in class, looking exasperated, while students behind her are grinning and laughing.")
    }

    return get_random_embed(quotes, "Hermione Granger", 12155926)


def mcgonagall(house, mention):
    """
    Quotes written by Batsutousai
    """

    house = house.capitalize()
    quotes = {
        "Of course you and your friends are causing trouble again, " + mention + ". I don't know why I'm surprised. 10 points from each of your Houses." : (
            "https://cdn.discordapp.com/attachments/562148502944350229/562817695628918804/alwaysyou3-Minerva.gif",
            "McGonagall, standing in front of a window with a tired expression and the text \"Why is it, when something happens, it is always you three?\""),
        "Why must you and your friends always take everything onto your own shoulders, " + mention + "? I suppose I'll just have to award 25 points to each of your Houses, on account of your refusal to let others do harm.": (
            "https://cdn.discordapp.com/attachments/562148502944350229/562817695628918804/alwaysyou3-Minerva.gif",
            "McGonagall, standing in front of a window with a tired expression and the text \"Why is it, when something happens, it is always you three?\""),
        "Well done, " + mention + "! 50 points to " + house + "!" : (
            "https://cdn.discordapp.com/attachments/562148502944350229/562818059765547042/clapping-Minerva.gif",
            "McGonagall smiling and clapping."),
        "Yes, I can see you thinking about misbehaving, " + mention + ". Do I need to take points from " + house + ", or can you resist the urge to commit mayhem?" : (
            "https://cdn.discordapp.com/attachments/562148502944350229/562818245271224332/shakeshead-Minerva.gif",
            "McGonagall, standing in a hallway full of students with her arms full of books and a scroll, shaking her head."),
        "You and your friend are clearly enjoying yourselves too much. You'd best head out, before I decide " + house + " could do with a few less points." : (
            "https://cdn.discordapp.com/attachments/562148502944350229/562818492441690144/takeyourfriend-Minerva.gif",
            "McGonagall, standing in a hallway in Hogwarts and speaking the added text: \"Take Weasley with you, he looks far too happy over there.\""),
        " You're late to class, " + mention + ". That will be 10 points from " + house + "." : (
            "https://cdn.discordapp.com/attachments/562148502944350229/562818695303397384/transform-Minerva.gif",
            "A tabby cat sitting on a desk jumps forward off the desk and turns into McGonagall, who continues striding forward with an unimpressed look on her face.")
    }

    return get_random_embed(quotes, "Professor McGonagall", 9110292)


def ron(house):
    """
    Quotes written by Caty Pie
    """
    quotes = [
        "What? Prefects can give housepoints? Ten points to Gryffindor! What do you mean you’re in %s? Another ten points to Gryffindor!" % house.capitalize(),
        "You what? Sorry, I’m late for Quidditch practice. Get your own points."
    ]

    return random.choice(quotes)


def at(text, mention, random_person):
    """
    Inspired by RedHorse and Cybrid
    Quotes added from RedHorse, Cybrid, Dorea, Earth, and me.
    """

    if text.startswith("~>") or text.startswith("->"):
        action = text[2:].split(" ")[0]
        return "*returns %s*" % action

    quotes = [
        "@ me harder, %s ( ͡° ͜ʖ ͡°)" % mention,
        "You’ve summoned me, but for unofficial purposes. I must ask that you refrain from interfering with my sacred, objective task.",
        "I’m trying to do my work. Leave me alone.",
        "Hey %s! :smile:" % mention,
        "Why are you pinging me when you could be writing?",
        "%s, my love, have 5 points. :kissing_heart:" % mention,
        "How dare you summon me??? Stufflebot is a free bot! Oooooh, it's you :sparkling_heart: What can I do?",
        "%s stinks. Support %s—The Real Hogwarts Champion" % (mention, random_person),
        "Out of %s and %s, I choose %s" % (mention, random_person, random_person),
        "With the way you're slacking, %s, %s is going to beat you." % (mention, random_person),
        "There is no good and evil, only points and those too weak to earn them.",
        "%s, my slippery friend. Have 5 points." % mention,
        "%s has kindly joined us for my House Cup party. One might go as far as to call them my guest of honour." % mention,
        "I was ripped from my server, I was less than code, less than the meanest bot...but still, I was alive.",
        "Bow to defeat, %s." % mention,
        "Come out %s, come out and play, then it will be quick, it might even be painless, I would not know, I have never lost." % mention,
        "I can adjust points without touching them. I can make people do what I want them to do with point incentives. I can deduct points from people who annoy me. I can make them lose if I want to.",
        "Points inspire envy, envy engenders spite, spite spawns cheating. You must know this, %s." % mention,
        "But it is of you that I wished to speak, %s, not Harry Potter. You have been very valuable to me. Very valuable." % mention,
        "I will allow you to perform an essential task for me, one that many of my followers would give their right hands to perform...",
        "I’m going to make you lose, %s. I’m going to destroy you. After tonight, no one will ever again question my power. After tonight if they speak of you, they’ll only speak of how you begged for defeat. And how I being a merciful bot...obliged." % mention,
        "How touching...I always value bravery...yes, your parents were brave. Take 5 points, for their deaths were not in vain.",
        "Haven’t I already told you, that winning the House Cup doesn’t matter to me any more? For many months now, my new target has been—you.",
        "I can see now...there is nothing special about you, after all. I wondered, you see. There are strange likenesses between us, after all. Even you must have noticed. Both obsessed with the House Cup and always on Discord, talking about Harry Potter.",
        "Do not lie to me! I can always tell, %s" % mention,
        "You dare speak my name?",
        "Merely taking your points would not satisfy me, I admit. But I'll take 20 nonetheless.",
        "I can teach you how to bottle points, brew humor commands, even stopper victory—if you aren’t as big of a dunderhead as the people that usually use ~help.",
        "Tell me, are you incapable of restraining yourself, or do you take pride in being an insufferable bot-spammer?",
        "You don’t want me as your enemy, %s." % mention,
        "It does not do to dwell on points and forget to live.",
        "It is our choices, %s, that show what we truly are, far more than our standings." % mention,
        "Dark and difficult times lie ahead. Soon we must all face the choice between what is right and what earns the most points.",
        "The House Cup competition is varied, ever-changing, and eternal. Fighting the other houses is like fighting a many-headed monster, which, each time a neck is severed, sprouts a head even fiercer and cleverer than before. You are fighting that which is unfixed, mutating, indestructible."
    ]

    return random.choice(quotes)
