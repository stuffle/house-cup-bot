import random


def inspireme():
    """
    Responses written by Stuffle, Dorea, and Caty
    """
    facts = [
        "Ed Sheeran bought a ticket to LA with no contacts. He was spotted by Jamie Foxx, who offered him the use of his recording studio and a bed in his Hollywood home for six weeks.",
        "In 2009, Stephen Hawking held a reception for time travelers, but didn’t publicize it until after. This way, only those who could time travel would be able to attend.",
        "In Svalbard, a remote Norwegian island, it is illegal to die because bodies are unable to be buried safely due to the permafrost on the ground. If you are about to die, they fly you back to mainland Norway to pass on there.",
        "When George Washington died, Napoleon Bonaparte of France gave a personal eulogy and ordered a ten day mourning period for France.",
        "Scientists discovered sharks that are living in an active underwater volcano. Divers cannot investigate because they would get burns from the acidity and heat.",
        "To properly write adjectives in order, you would list them by amount, value, size, temperature, age, shape, color, origin, and material."
    ]

    quotes = [
        "Neil Gaiman: I’m not going to tell you how to feel, I’m going to kill that unicorn and I’m going to break your heart.",
        "Neil Gaiman: You learn more from finishing a failure than writing something fantastic that you never finish.",
        "Franz Kafka: Follow your most intense obsessions mercilessly.",
        "Octavia E. Butler: You don’t start out writing good stuff. You start out writing crap and thinking it’s good stuff, and then gradually you get better at it.\nThat’s why I say one of the most valuable traits is persistence.",
        "Jodi Picoult: You can always edit a bad page. You can’t edit a blank page."
        "Dumbledore: Of course it is happening inside your head, Harry, but why on Earth should that mean it’s not real?",
        "Dumbledore: Words are, in my not so humble opinion, our most inexhaustible source of magic.",
    ]

    humour = [
        "If you’re stuck for ideas, remember the werechair.",
        "Why does inspiration always come when I should be sleeping?? :sweat:",
        "Don’t write anything Tom wouldn’t do.",
        "Just, whatever you do, don’t let Tom play with knives... :sweat:",
        "Harry in a dress!\nI’m just saying...",
        "Whatever you have planned, don’t worry about it. I’m sure Harry won’t mind...",
        "Just relax your shoulders, close your eyes, and take a deep, calming breath. Don’t let the smell of chloroform bother you.",
        "You might not like my advice. It involves cable ties and a very firm paddle.",
        "If all else fails, get them all drunk.",
        "\n“Roses are red,\nViolets are blue,\nI have a gun,\nGet in the van.”\n*(Dory’s example of Tom’s poetic prowess.)*",
        "I think Harry needs a hug! :heart:",
        "There’s nothing wrong with a little kidnapping between friends."
    ]

    inspirations = [
        "Sometimes the best thing you can do is walk away and come back later.",
        "When I go fishing for inspiration, I always remember my rod. :fishing_pole_and_fish:",
        "\nWith every word you add, you’re one word closer to finishing.\n" \
        "With every word you change, you’re that little bit more concise.\n" \
        "With every word you take away, you’re that much closer to your final vision.\n" \
        "So just keep going, one word at a time.",
        "I know you can do it. You just have to believe in yourself like I believe in you. :kissing_heart:",
        "When you get stuck, ask yourself, ‘What do my characters want?’ \nBut regardless of what they want, when you get to the end, make sure you give them what they *need*."
    ]

    responses = facts + quotes + humour + inspirations
    return random.choice(responses)
