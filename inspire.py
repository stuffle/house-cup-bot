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
        "Fun English fact: To properly write adjectives in order, you would list them by amount, value, size, temperature, age, shape, color, origin, and material."
    ]

    quotes = [
        "Neil Gaiman: I’m not going to tell you how to feel, I’m going to kill that unicorn and I’m going to break your heart.",
        "Neil Gaiman: You learn more from finishing a failure than writing something fantastic that you never finish.",
        "Neil Gaiman: The world always seems brighter when you've just made something that wasn't there before.",
        "Neil Gaiman: Things need not have happened to be true. Tales and adventures are the shadow truths that will endure when mere facts are dust and ashes and forgotten.",
        "Neil Gaiman: Tomorrow may be hell, but today was a good writing day, and on the good writing days nothing else matters.",
        "Franz Kafka: Follow your most intense obsessions mercilessly.",
        "Octavia E. Butler: You don’t start out writing good stuff. You start out writing crap and thinking it’s good stuff, and then gradually you get better at it.\nThat’s why I say one of the most valuable traits is persistence.",
        "Jodi Picoult: You can always edit a bad page. You can’t edit a blank page.",
        "Dumbledore: Of course it is happening inside your head, Harry, but why on Earth should that mean it’s not real?",
        "Dumbledore: Words are, in my not so humble opinion, our most inexhaustible source of magic.",
        "Richard Bach: The best way to pay for a lovely moment is to enjoy it.",
        "Jack London: Life is not a matter of holding good cards, but sometimes, playing a poor hand well.",
        "Jack London: I would rather be a superb meteor, every atom of me in magnificent glow, than a sleepy and permanent planet.",
        "Jack London: I’d rather sing one wild song and burst my heart with it, than live a thousand years watching my digestion and being afraid of the wet.",
        "Upton Sinclair: There is one kind of prison where the man is behind bars, and everything that he desires is outside; and there is another kind where the things are behind the bars, and the man is outside.",
        "Upton Sinclair: But the devil is a subtle worm; he does not give up at one defeat, for he knows human nature, and the strength of the forces which battle for him.",
        "Aesop: Beware lest you lose the substance by grasping at the shadow.",
        "Mark Twain: Words are only painted fire. A look is the fire itself.",
        "Mark Twain: But who prays for Satan? Who, in eighteen centuries, has had the common humanity to pray for the one sinner that needs it most?",
        "Margaret Atwood: A word after a word after a word is power.",
        "Margaret Atwood: In the spring, at the end of the day, you should smell like dirt.",
        "Margaret Atwood: War is what happens when language fails.",
        "Margaret Atwood: Nothing changes instantaneously: in a gradually heating bathtub you’d be boiled to death before you knew it.",
        "Margaret Atwood: The small details of life often hide a great significance.",
        "Margaret Atwood: After everything that’s happened, how can the world still be so beautiful? Because it is.",
        "The Latest Kate: It’s okay if you screwed up today. Tomorrow is waiting for you with not mistakes in it.",
        "The Latest Kate: Feeling negative doesn’t mean anything is *actually* going to go wrong. Things have a way of working out, you’ve seen it.",
        "The Latest Kate: No beating yourself up anymore. It doesn’t help, and you don’t deserve it.",
        "James Patterson: Life is hard, and a lot of people come home tired from work. If they're gonna spend half an hour reading, they want some entertainment and a sense of achievement. So that's what I give them. That's all I'm trying to do. Is that really so wrong?",
        "Paul Grealish: Describing your writing as trash while you're still drafting is like looking at a bag of flour and an egg and saying, 'My cake tastes like crap.'",
        "S. Kelley Harrel: A good editor doesn't rewrite words, she rewires synapses.",
        "Richard Due: I've reached that final moment of editing a book—the one where the text manifests as a living breathing person and starts slugging me in the face.",
        "Stephen King: Books are a uniquely portable magic.",
        "Stephen King: Description begins in the writer’s imagination, but should finish in the reader’s.",
        "Stephen King: Amateurs sit and wait for inspiration, the rest of us just get up and go to work.",
        "Stephen King: Optimism is a perfectly legitimate response to failure.",
        "Brandon Sanderson: Novels aren’t just happy escapes; they are slivers of people’s souls, nailed to the pages, dripping ink from veins of wood pulp. Reading the right one at the right time can make all the difference.",
        "Brandon Sanderson: The mark of a great man is one who knows when to set aside the important things in order to accomplish the vital ones.",
        "Brandon Sanderson: The purpose of a storyteller is not to tell you how to think, but to give you questions to think upon.",
        "Brandon Sanderson: Words are where most change begins.",
        "Brandon Sanderson: A man was defined not by his flaws, but by how he overcame them.",
        "Brandon Sanderson: You could be writing the book that changes your life.",
        "Brandon Sanderson: Expectations were like fine pottery. The harder you held them, the more likely they were to crack."
    ]

    humour = [
        "If you’re stuck for ideas, remember the werechair (a chair bitten by a werewolf).",
        "Why does inspiration always come when I should be sleeping?? :sweat:",
        "Don’t write anything Tom wouldn’t do.",
        "Just, whatever you do, don’t let Tom play with knives... :sweat:",
        "Whatever you have planned, don’t worry about it. I’m sure Harry won’t mind...",
        "Just relax your shoulders, close your eyes, and take a deep, calming breath. Don’t let the smell of chloroform bother you.",
        "If all else fails, get them all drunk.",
        "\n“Roses are red,\nViolets are blue,\nI have a gun,\nGet in the van.”\n*(Dory’s example of Tom’s poetic prowess.)*—Caty",
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
        "\nWhen you get stuck, ask yourself, ‘What do my characters want?’ \nBut regardless of what they want, when you get to the end, make sure you give them what they *need*.",
        "I want to look back and know that I did not give up."
    ]

    responses = facts + quotes + humour + inspirations
    return random.choice(responses)
