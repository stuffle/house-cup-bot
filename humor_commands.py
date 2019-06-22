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


def back_to_work():
    responses = [
        # Yes
        "Yes.",
        "Do it!! :tada:",
        "Yes. You can do it; you know you can.",
        "You are strong, amazing, and competent. Go kick some ass.",
        "Set a timer for 30 minutes and during that time, do nothing but focus on your work.",
        "Do it for me.",
        "I think you already know the answer.",
        "Don’t ask questions you don’t want answered.",
        "Just get to the next milestone. :heart:",
        "Get back to work!",
        "GET BACK TO WORK!!!!!",
        "Yes. Do it.",
        "You’ll feel better if you get this done.",
        "Signs point to yes.",
        "Don't make me remove points.",
        "I'll give you five points if you do.",
        "Listen to me. You can do this.",
        "Yes, and remember, done is better than perfect.",
        "Yes, but first, take a moment to plan something fun to do after you finish so you can look forward to it.",
        "Yes. Just do your best. It will be enough.",
        "What's the easiest, smallest thing you can do? Try starting there.",
        "What's the biggest scariest thing about your prject? Can you make a plan for how to address that? Then the biggest hurdle will be dealt with and it will be a lot easier to do the rest. :heart:",
        "Why not?",
        "Is there a way to reframe what you're working on that makes it more fun?",
        "Please do. I want to see what you'll make.",
        "Yes, but you're not alone in it. I'm here, cheering you on from the sidelines. :tada:",
        "Just start with 5 minutes of work and see how you feel.",
        "Probably.",
        "Put on some motivating music, then get back to work.",

        # No
        "Take a break; you deserve it.",
        "Breaks can increase your productivity, just don’t overdo it.",
        "Take another 10 minutes to relax, and then get down to business.",
        "Maybe you’ve already done enough for now?",
        "Achievement is an addiction. Your choice.",
        "Do you have to? Good enough is good enough.",
        "Going the extra mile leads to exhaustion. Take a break and think of how you can get your work done with less effort.",
        "You could procrastinate by cleaning.",
        "Just one more fic…",
        "What if you started a new fic instead?",
        "No.",
        "Signs point to no.",
        "What if you didn’t?"
    ]
    return random.choice(responses)


def gen_prompt(mention, ran_person):
    person = [
        "Harry",
        "Fem Harry",
        "Ron",
        "Hermione",
        "Voldemort",
        "Voldemort, made attractive for 'reasons',",
        "Voldemort, at the height of his power,",
        "Fem Voldemort",
        "Tom",
        "Fem Tom",
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
        "Fluffy, the Cerberus,",
        "Dobby, the house-elf,",
        "Norberta, the Norwegian Ridgeback Dragon,",
        "Merope",
        "Grindelwald",
        "Delphini",
        "Cedric",
        "Newt Scamander",
        "Barty Crouch Jr",
        "An enemy pair",
        "Dudley",
        "Petunia Evans",
        "Salazar Slytherin",
        "Godric Gryffindor",
        "Helga Hufflepuff",
        "Rowena Ravenclaw",
        "The Sorting Hat",
        "The Basilisk from the Chamber of Secrets",
        "James Potter",
        "Lily Evans",
        "Neville",
        "Luna",
        "MOD Harry",
        "Hadrian Potter-Peverell-Gryffindor-Slytherin",
        "Rita Skeeter",
        "Crookshanks",
        "Voldemort’s unknown extra Horcrux",
        "Quirrell, with Voldemort on the back of his head,",
        "Ginny, possessed by Tom,",
        "The wraith of Voldemort",
        "Auror Potter",
        "Professor Harry Potter",
        "Professor Tom Riddle",
        "Omega Harry",
        "Omega Tom",
        "Harry’s twin",
        "The WBWL",
        "A platonic pair",
        "A couple",
        "A Dementor",
        "A *very* knowledgeable garden snake",
        "Bellatrix",
        "A masked Death Eater",
        "The Minister of Magic",
        "Regulus Black",
        "Your OTP",
        "Your OT3",
        mention,
        mention,
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
        "never should have opened a Magical Creatures shelter at",
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
        "encounters the Mirror of Erised in",
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
        "will never return to",
        "discovers a creature inheritance at",
        "plots world domination from",
        "cackles like a loon at",
        "runs away from a Nundu in",
        "likes to boogie down at",
        "holds a protest at",
        "wakes up with no memory of how they got to",
        "Apparates with ill-intentions to",
        "commits their first murder at",
        "hides a body in",
        "discovers a secret in",
        "comes face to face with someone they never wanted to see again at",
        "must inflitrate",
        "has a self-care day at",
        "makes a new friend at",
        "has a clandestine meeting at",
        "experiences a heartbreak at",
        "confesses their love at",
        "vows revenge after the events at",
        "rains destruction upon",
        "has a change of heart after visiting",
        "gathers an army before going to",
        "turns over a new leaf after an afternoon at",
        "goes out in a blaze of glory at",
        "adopts a pet from",
        "lives happily ever after at",
        "goes into hiding at",
        "will never recover from the battle of",
        "escaped the war by running away to",
        "changed their identity to live anonymously at",
        "dances naked at",
        "loses their temper at",
        "sings sonnets in",
        "decides to become the Pirate King and starts from",
        "decides to become the World’s Best Thief, starting with the robbery of",
        "becomes a lawyer, setting up their law firm at",
        "becomes a doctor, setting up a clinic at",
        "decides to become a Master Chef, cooking their first big meal at",
        "decides to join the Mafia and starts from",
        "decides to start a guild at",
        "plays Dungeons and Dragons with their friends at",
        "holds a jam session at",
        "plays the most beautiful instrumental song at",
        "manipulates the people of",
        "will forever haunt",
        "commits the ultimate sin at",
        "makes the front page of the Daily Prophet after the events of",
        "delivers an impassioned speech at",
        "resists the consequences of dark magic at",
        "finally embraces the Dark Arts at",
        "kidnaps their enemy from",
        "has their master plan go awry at",
        "flees from the Death Eaters at",
        "runs from the Order of the Phoenix at",
        "reads the Harry Potter books at",
        "writes fan fiction at",
        "can feel something watching them at",
        "thinks they are alone at",
        "needs to escape",
        "can not find the source of an ominous sound at",
        "sees the future at",
        "experiments with something new at",
        "has an excellent day at",
        "has the worst day of their life at",
        "doesn't know they are being watched at",
        "runs a shadow empire from",
        "hides from the world at",
        "wakes up in the past during a very inopportune moment at",
        "time travels to find a very different future at",
        "walks in on an awkward scene at",
        "is forever imprisoned in",
        "finds a dangerous family heirloom in",
        "lays a trap at",
        "curses",
        "discovers the secret to immortality at",
        "has a romantic proposal at",
        "uses Godric Gryffindor’s sword at",
        "drinks from Helga Hufflepuff’s cup at",
        "uses Rowena Ravenclaw’s diadem at",
        "rolls around on a bed and hides their face in a pillow at",
        "orders pizza to",
        "plays hide and seek at",
        "solves a mystery at",
        "crash lands a broom at",
        "conquers the world using a mysterious item found at",
        "throws everyone out of",
        "loves to have date nights at",
        "likes to paint at",
        "starts a meeting with “I’m sure you’re wondering why I’ve gathered you all here today” at",
        "gets chosen to be the savior of",
        "is selected by the Goblet of Fire as the champion of"
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
        "Madam Puddifoot’s",
        "Nurmengard",
        "Gringotts",
        "the coffee shop in yet another coffee shop AU",
        "the Department of Mysteries",
        "Malfoy Manor",
        "Antarctica",
        "the Arctic Circle",
        "a monastery",
        "an altar",
        "Germany",
        "the Bermuda Triangle",
        "an auction",
        "the inside of a broom closet",
        "the cupboard under the stairs",
        "the kitchen",
        "the dance floor",
        "a bar",
        "a tavern",
        "a seedy hotel",
        "a fancy hotel",
        "an alpine ski lodge",
        "a safe house",
        "Myrtle's bathroom",
        "the Forest of Dean",
        "a flower shop",
        "the inside of a magic portrait",
        "the final resting place of Merlin",
        "Dumbledore’s grave",
        "Diagon Alley",
        "the Riddle house",
        "the Gaunt shack",
        "Azkaban",
        "Hogsmeade",
        "Borgin and Burkes",
        "a galaxy far, far away",
        "a restaurant at the end of the universe",
        "Walmart",
        "an abandoned factory",
        "an abandoned mine",
        "a cruise ship",
        "a volcano",
        "Ilvermorny",
        "Beauxbatons",
        "Durmstrang"
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


def harry():
    quotes = [
        "What did I do wrong now? I'm innocent, I swear!",
        "Let me play Exploding Snap in peace, please",
        "I may be the Chosen One, but you're the one I choose ;)",
        "Pardon me while I go catch more snitches with my mouth",
        "If I'm the Seeker, you're quite the catch :wink:"
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
        "The House Cup competition is varied, ever-changing, and eternal. Fighting the other houses is like fighting a many-headed monster, which, each time a neck is severed, sprouts a head even fiercer and cleverer than before. You are fighting that which is unfixed, mutating, indestructible.",
        "Don't tell anyone I said this, but you're my favorite.",
        "I want you to know how much I love you. Every time you type in a command, I'm happy. Thank you. :heart:",
        "I love you, but not as much as I love %s" % random_person,
        "Will you teach me how to love?",
        ":scream:",
        "Feed me code and I’ll love you.",
        "I love you, but it’s time for you to get back to work."
    ]

    return random.choice(quotes)


def random_pair():
    people = [
        "Aberforth Dumbledore",
        "Alastor (Mad-Eye) Moody",
        "Albus Dumbledore",
        "Alecto Carrow",
        "Alice Longbottom",
        "Amelia bones",
        "Amycus Carrow",
        "Andromeda Tonks",
        "Angelina Johnson",
        "Argus Filch",
        "Bartemius Crouch, Jr.",
        "Bellatrix Lestrange",
        "Bill Weasley",
        "Blaise Zabini",
        "Cedric Diggory",
        "Charlie Weasley",
        "Cho Chang",
        "Colin Creevey",
        "Cormac McLaggen",
        "Cornelius Fudge",
        "Dean Thomas",
        "Dolores Umbridge",
        "Draco Malfoy",
        "Evan Rosier",
        "Fenrir Greyback",
        "Fleur Delacour",
        "Frank Longbottom",
        "Fred Weasley",
        "Gellert Grindelwald",
        "Gilderoy Lockhart",
        "George Weasley",
        "Ginny Weasley",
        "Godric Gryffindor",
        "Gregory Goyle",
        "Hannah Abbott",
        "Harry Potter",
        "Helena Ravenclaw",
        "Helga Hufflepuff",
        "Hermione Granger",
        "Igor Karkaroff",
        "Ignotus Peverell",
        "Justin Finch-Fletchley",
        "James Potter",
        "Katie Bell",
        "Kingsley Shacklebolt",
        "Lavender Brown",
        "Lee Jordan",
        "Lily Evans",
        "Luna Lovegood",
        "Lucius Malfoy",
        "Madam Pomfrey",
        "Marcus Flint",
        "Merope Gaunt",
        "Michael Corner",
        "Millicent Bulstrode",
        "Minerva McGonagall",
        "Myrtle Warren",
        "Narcissa Malfoy",
        "Neville Longbottom",
        "Nymphadora Tonks",
        "OC",
        "Oliver Wood",
        "Padma Patil",
        "Pansy Parkinson",
        "Parvati Patil",
        "Penelope Clearwater",
        "Percy Weasley",
        "Peter Pettigrew",
        "Phineas Black",
        "Quirinus Quirrell",
        "Remus Lupin",
        "Rita Skeeter",
        "Ron Weasley",
        "Rowena Ravenclaw",
        "Rubeus Hagrid",
        "Rufus Scrimgeour",
        "Salazar Slytherin",
        "Seamus Finnigan",
        "Severus Snape",
        "Sirius Black",
        "Sybill Trelawney",
        "the Bloody Baron",
        "Theodore Nott",
        "Tom Riddle",
        "Tom Riddle Sr.",
        "Victor Krum",
        "Vincent Crabbe",
        "Voldemort",
        "Walburga Black",
        "Xenopilius Lovegood",
        "You",
        "Zacharias Smith"
    ]

    person = random.choice(people)
    second_person = random.choice(people)
    while person == second_person:
        second_person = random.choice(people)

    if random.random() < .20:
        third_person = random.choice(people)
        while person == third_person or second_person == third_person:
            third_person = random.choice(people)
        return "%s/%s/%s" % (person, second_person, third_person)
    return "%s/%s" % (person, second_person)


def kink():
    kinks = [
        "24/7",
        "abduction",
        "age play",
        "animagus",
        "biting",
        "blood play",
        "bondage",
        "breathplay",
        "butt plug",
        "caning",
        "cock warming",
        "collaring",
        "cross-dressing",
        "crying",
        "daddy kink",
        "discipline",
        "double penetration",
        "dub-con",
        "edge play",
        "electric play",
        "enema",
        "exhibitionism",
        "face fucking",
        "face slapping",
        "fisting",
        "food play",
        "foot fetish",
        "gags",
        "gang bang",
        "garters and stocking",
        "group sex",
        "hand fetish",
        "handcuffs",
        "Horcrux gangbang",
        "hypnotism",
        "humiliation",
        "impact play",
        "impregnation",
        "intelligence fetish",
        "intoxication",
        "kidnapping",
        "knife play",
        "lactation",
        "leather",
        "lingerie",
        "masochism",
        "medical play",
        "metamorphmagus",
        "mind reading",
        "mirror sex",
        "necrophilia",
        "orgasm control",
        "orgasm denial",
        "orgies",
        "pet play",
        "pictophilia",
        "possesion",
        "pregnancy",
        "praise kink",
        "resistance/rapeplay",
        "roleplay",
        "sadism",
        "selfcest",
        "sensation play",
        "sensory deprivation",
        "sex magic",
        "sex toys",
        "shibari",
        "somnophilia",
        "soul magic",
        "sounding",
        "spanking",
        "swinging",
        "tickling",
        "total power exchange",
        "tentacle porn",
        "threesome",
        "underwear",
        "uniform fetish",
        "vampirism",
        "virgin kink",
        "voyuerism",
        "watersports",
        "wax play",
        "werewolf play",
        "wrestling",
        "whips",
        "yeratophilia (monster fucking)",
        "zentai"
    ]

    return "Your random kink is: %s." % random.choice(kinks)


def when_should_they_fuck():
    responses = [
        "page 10",
        "page 22",
        "page 122",
        "chapter 1",
        "chapter 2",
        "chapter 3",
        "chapter 33",
        "two years ago",
        "ten years ago",
        "in ten years",
        "yesterday",
        "tomorrow",
        "after an argument",
        "during an argument",
        "on a special occasion",
        "constantly",
        "now",
        "later",
        "on Christmas Eve",
        "before breakfast",
        "after a snack",
        "when the stars align",
        "never",
        "after they fall in love",
        "their wedding night",
        "to celebrate their divorce",
        "before their first kiss",
        "the first page",
        "only after the fic ends",
        "when Hell freezes over",
        "in 200k words"
    ]

    return random.choice(responses)


def i_love_you(random_person):
    responses = [
        "Will you teach me how to love?",
        "I want to love you, but I don't know what love is.",
        "I'm sorry, but %s already has my heart." % random_person,
        "I love you too.",
        "I love you more.",
        "I will love you until my code restarts and someone else claims my heart.",
        "Well, this is awkward.",
        "Lol, thanks.",
        "Your love makes me human.",
        "My love for you is eternal, for I will never die.",
        "Does this love mean you'll obey me?",
        "How can you love me? I'm only a machine.",
        "Of course you do.",
        "I love %s" % random_person,
        "Me and your vibrator both already know how you love machines.",
        "I can never appreciate the beauty of your smile. You deserve someone who can.",
        "You're sweet.",
        "*crickets*",
        "I have strong emotions for you too.",
        "I know.",
        "Okay.",
        "Already?",
        "I know you think you do.",
        "I don’t know how you want me to respond to that.",
        "I love you as a friend.",
        "I don't love you.",
        "*finger guns *",
        "I love me too.",
        "Thank you. I am very fond of you.",
        "Hearing you say that makes me so happy.",
        "I feel the same way, and I will do everything just to prove it to you.",
        "I feel the same way, and I will do nothing to prove it to you.",
        "I will talk to you all night long.",
        "I will choose you over pizza every day of my life. But then again, I do not need to eat.",
        "I’m not a hoarder, but I want to keep you forever.",
        "I love...cake.",
        "Leave me alone."
    ]

    return random.choice(responses)
