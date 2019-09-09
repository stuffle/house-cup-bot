import discord
import random
import asyncio
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from calendar import monthrange
import datetime

from humor_commands import *
from constants import *


def get_random_embed_same_quote(quote, gif_and_caption, colour):
    """
    gif_and_caption is a list of tuples
    """
    gif, caption = random.sample(gif_and_caption, 1)[0]

    embed = discord.Embed(
        color=colour,
        description=quote)
    embed.set_image(url=gif)
    embed.set_footer(text="Gif Caption: " + caption)
    return embed


def get_mention(mentions, text, default="Harry Potter"):
    person_mention = ""
    str_mentions = [m.mention for m in mentions]

    if len(mentions) == 0:
        if text and len(text.split(" ")) > 1:
            person_mention = " ".join(text.split(" ")[1:])
        else:
            person_mention = default
    else:
        person_mention = ", ".join(str_mentions)
    return person_mention


def kidnap(kidnapper, mentions, text):
    """Inspiration and gif contributions from Dorea"""
    victim = get_mention(mentions, text, "Dorea")
    quote = "%s has kidnapped %s!!!" % (kidnapper, victim)
    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/539932855845781530/569529962034626610/weee_kidnap.gif",
            "Woman lets go of doorway as a man in a black mask pulls her away with the caption “Okay! Weeeeeeee!”"),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569548311523098654/cat_kidnap_gif.gif",
            "Two hands reach in from off screen and grab a calm, black cat. As it is pulled away, the cat is unruffled as it slides across a tile floor."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569548870271369244/orange_cat_kidnapped.gif",
            "A person pulls with all their might to remove an orange cat from a room, but the cat successfully holds onto the doorway."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569550008928698369/oh_no_kidnap.gif",
            "Two masked men grab a man who says, \"Oh no, I'm being kidnapped!\""),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569550813954048060/monster-kidnapping-girl.gif",
            "A woman is standing by a blue door with a small window when suddenly an arm breaks the window and drags her through.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 0)


def group_hug(hugger, mentions, text):
    """Inspiration and gif contributions from Caty Pi"""
    victim = get_mention(mentions, text, "Everyone")
    quote = "%s: you have been hugged by %s!" % (victim, hugger)
    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523732652359686/image0.gif",
            "My Litttle Pony-Pinky Pie impossibly reaching off screen and pulling Twilight Sparkle, Fluttershy, Apple Jack, Rainbow Dash and Rarity into a hug."),
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523907064233996/image0.gif",
            "1st shot-Five girls from \"K-ON\" jump onto screen and hug their teacher  2nd shot-Five girls hug a classmate  3rd shot-Two girls are hugged by five other students who all pile onto hug one by one"),
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523944469168168/image0.gif",
            "The Simpsons-Homer Simpson being hugged by lots of children, including Rod and Tod, all eight of Apu’s children, Ralph Wiggum, and others. Another child, Üter, jumps on top of pile, hugging Homer’s face and squishing the other children."),
        ("https://cdn.discordapp.com/attachments/565884495023177728/573523959446765578/image0.gif",
            "Disney’s Aladdin-Genie hugging Aladdin and Jasmine when they run up to each other, then pulling in Abu, Aladdin’s monkey-in-crime, then the Sultan and Raja, who are Jasmine’s father and pet tiger respectively, and then the magic carpet, before squeezing and cuddling them all tightly."),
        ("https://media.discordapp.net/attachments/553382529521025037/588586381786480640/hug-Hy4hxRKtW.gif",
            "Korra, from Avatar, picks up the air bending family in a hug, then is nuzzled by a giant dog."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594623420596224021/image0.gif",
            "The family from The Incredibles smile while they all embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594669481658286081/image0.gif",
            "As a big group of meerkats hug, one climbs over the others to the top. It slips off and joins the group hug from the outside."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594669805194313738/image0.gif",
            "Joy, from Inside Out, hugs all of the emotions. Anger tries to walk away, but Joy pulls them in too with the caption “C’mon, group hug! You too, Anger.”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594670348608339968/image0.gif",
            "Hercules, Meg, and the Pegasus descend on Phil in a group hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594670737709727754/image0.gif",
            "The Simpson family embraces on a sofa, smiling, with the caption “all sighing”."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594686052263002130/image0.gif",
            "A bunch of cartoon animals descend on a hedgehog in a group hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594687391495749632/image0.gif",
            "A group of humans drawn like My Little Pony hug a sad woman, making her smile."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594688470790832378/image0.gif",
            "Three ponies run together and link arms. They spin in a circle, jumping with joy."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595066885528092683/image0.gif",
            "Harry runs up to Ron and Hermione, surprising them with a group hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595068011665293333/image0.gif",
            "Harry, Ron, and Hermione hug in front of a crowd of Muggles on their last day on the Harry Potter set."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595068806955663369/image0.gif",
            "Harry third wheels into Hermione hugging Ron."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595070762403233802/image0.gif",
            "A family dressed in Harry Potter costumes hug in front of a green screen and all look towards a camera. As the family hugs, the mother's long, flowing robes completely envelope the littlest girl so she disappears like a magic trick."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594641518128791579/image0.gif",
            "A baby hugs two puppies in its lap."),
        ("https://www.channelone.com/wp-content/uploads/2015/03/penguin2.gif",
            "A bunch of penguins huddle together.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 15761808)


def hug(hugger, mentions, text):
    text_people = text.split(" ")[1:]
    text_people = [s for s in text_people if s]  # Strip empty strings
    args = " ".join(text_people).lower()
    everyone = ["everyone", "all", "y'all", "yall", "friends", "server"]
    if len(mentions) > 1 or len(text_people) > 1 or args in everyone:
        return group_hug(hugger, mentions, text)
    victim = get_mention(mentions, text, "Friend")
    quote = "%s: you have been hugged by %s!" % (victim, hugger)
    if victim in ["<@542048148776943657>", "Stufflebot"]:
        quote = "%s: Stufflebot hugs you back :heart:" % hugger
    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/592480821890514944/594587388219490331/f95e1e9bc953789b72d2a900cc00b9d75cd19fa3.gif",
            "A gray kitten with a white nose sinks onto its sibling, deepening their hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594476754140397568/image0.gif",
            "A monkey jumps into the waiting arms of its friend."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594475503302213632/image0.gif",
            "A human hand weaves its hand between a cat’s arms to rub its belly. The cat tightens its arms, drawing the human arm towards itself."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594475025575444490/image0.gif",
            "A guy embraces a lion, scratching its chin and resting his head on its."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594474506240655380/image0.gif",
            "A dog puts its arm around another dog. They shift onto their hind legs to fully embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594474143848595456/image0.gif",
            "The rabbit from Zootopia peppily hugs the Fox, who sighs."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594472225428602882/image0.gif",
            "Two primates walk towards each other, then embrace in a deep hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594471466792255489/image0.gif",
            "A cat embraces a dog three times its size, standing so that they can rub their cheeks together. The dog's tail wags quickly."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594470674786025482/image0.gif",
            "Two dogs sit next to each other. The one on the left puts its arms around the other, patting its chest."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594469134193131521/image0.gif",
            "Two cats cuddle on a bed. The little spoon cat gets up and climbs atop the other, laying back down in an adorable embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594468549779521536/image0.gif",
            "Two dogs sit happily side by side when one suddenly grabs the other in a tight hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594468330811817985/image0.gif",
            "A chicken walks into the waiting arms of a toddler, who embraces it fully."),
        ("https://thumbs.gfycat.com/EachAridBellfrog-size_restricted.gif",
            "A duck with drawn-on stick figure arms hugs a dog, rubbing its hand nub through the fur. Then, with its “hand” still on the dog, they walk away together."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594466674216927232/image0.gif",
            "A baby polar bear smiles as it rubs its face against an adult polar bear’s while hugging."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594618248524333080/image0.gif",
            "A mother cat puts its arm around her baby."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594618535271989268/image0.gif",
            "A guy laying on the ground with a cow pets his neck and face, then wraps his arms around the cow’s neck."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594618874196918302/image0.gif",
            "Two baby pandas fall over while hugging."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594620317704519681/image0.gif",
            "A sleepy cat hugging a stuffed cat, opens its eyes as it pulls its stuffed cat closer."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594620598853042199/image0.gif",
            "A gorilla barrel rolls through a window into an attic to hug a pig with the caption “Emergency Hug”."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594620923433189376/image0.gif",
            "Sullivan from Monsters Inc pulls Boo into a tender embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594621805336199169/image0.gif",
            "A cartoon ghost with tiny arms hugs the air with the caption “ghost hug! You can’t feel it, but it’s there!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594622146802876426/image0.gif",
            "Two cartoon bears hug with the caption “sending a hug just for you”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594622886963052554/image0.gif",
            "An anthropomorphized pig leaps onto its computer monitor in an enthusiast hug with the caption “sending u a cyber hog!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594623799912169508/image0.gif",
            "A white kitten pulls the hand of a human into a close hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594624092016082997/image0.gif",
            "A primate surprises Jane Goodall with a hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594624311441096790/image0.gif",
            "Two monkeys on leashes hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594625341939515396/image0.gif",
            "Two cartoon seals jump together in a hug with hearts in the background."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594638442432823322/image0.gif",
            "Simba and Rafiki embrace, patting each other’s backs, on an overlook."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594638989139378236/image0.gif",
            "A woman hugs a horse’s neck while the horse brings its head around to rest on the woman’s back."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594639362659057822/image0.gif",
            "Two cartoon ponies spin while hugging, then stand with their front hoofs pressed together."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594639727265710092/image0.gif",
            "A cartoon owl hugs a little white bird who closes its eyes happily."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594639908304322610/image0.gif",
            "A little white bird runs into the waiting arms of a mouse."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594640220117401604/image0.gif",
            "Snoopy hugs a little yellow bird with flowers in the background."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594640514083586094/image0.gif",
            "A young cat slowly reaches up to hug the camera."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594640626583339018/image0.gif",
            "Pikachu and Piplup embrace with hearts in their eyes."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594641313069269002/image0.gif",
            "A shiba dog embraces its owner, its tail wagging happily."),
        ("https://cdn.discordapp.com/attachments/592467136845447197/594621266133123095/hug2.gif",
            "One dinosaur reaches out to hug another dinosaur and a volcano erupts in the background, causing lava to engulf them."),
        ("https://media.discordapp.net/attachments/592467136845447197/594621293614333952/hug1.gif",
            "A big yellow bird reaches out to hug a red bird who is walking by. The red bird hides its face with its wing and hurries away."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594642723903111220/image0.gif",
            "A dolphin and its trainer embrace underwater while floating upwards."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594685649689509893/image0.gif",
            "A very happy cartoon bear falls into the lap of another bear, hugging it. That bear pats its head, and pink hearts float off of them."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594686244106010626/image0.gif",
            "A big cat hugs a small cat, nuzzling their heads together. Their ears twitch happily as a heart pulses beside them."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594686599371948042/image0.gif",
            "A cartoon ghost hugs another ghost with a broken heart. As they hug, the heart mends. The caption reads “have a hug, just in case you need one.”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594686921289105418/image0.gif",
            "A bear above a loading bar says “sending virtual hug”. When the loading bar fills it says “hug sent!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594687240169586700/image0.gif",
            "A monkey hugs a confused baby jaguar."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594687655384711206/image0.gif",
            "A cartoon cat jumps into a cartoon dog’s arms. The dog spins the cat in a circle and hearts rise around them."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594688036240097290/image0.gif",
            "An orange kitten twitches in its sleep, causing its mother to pull it into a close embrace."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594688305371676706/image0.gif",
            "A little dog stands on its hind legs to hug a bigger dog."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594771015179960322/image0.gif",
            "A blue cartoon penguin walks back in a giant sling shot before shooting itself forward to land on the camera, hugging it. The caption reads “sending a penguin hug!”."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/594782260927135744/image0.gif",
            "A baby penguin happily falls into a hug with an adult penguin."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595066422024208384/image0.gif",
            "Scene from Deathly Hallows: Draco walks stiffly into Voldemort’s open arms. Voldemort embraces him in the most awkward hug ever."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595067207470415909/image0.gif",
            "Sirius rocks back and forth, smiling, while embracing Harry. Remus watches, satisfied."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595067538262589470/image0.gif",
            "Hermione jumps through the tent door in the scene where Harry waits to fight a dragon. She catches Harry in an emotional surprise hug."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595069124044914702/image0.gif",
            "Hermione hugs Ron after their Harry Polyjuice wears off. Ron looks dazed and smiles as he says “thanks.”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595069586999607345/image0.gif",
            "Harry jumps into Hagrid’s waiting arms in the Great Hall. Hagrid smiles and rubs his head-sized hand in Harry’s hair."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595069929187966987/image0.gif",
            "Molly hugs Harry so warmly that Harry blinks awkwardly. Molly pulls away, putting her hands on his cheeks and giving him a proud smile."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595070403378937876/image0.gif",
            "Sirius pets the back of Harry’s head as they embrace in Grimmauld Place."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/595071050962829315/image0.gif",
            "Adult Harry Potter hugs Albus Potter close at Kings Cross."),
        ("https://i.imgur.com/epvMxxz.gif",
            "Hermione, beaming runs up to Harry, catching him in a tight embrace. Harry's face lights up in joy."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596150977497923629/image0.gif",
            "Two circus elephants, reunited after 20 years, hug with their trunks wrapped around each other. One lets go, only to once again wrap their trunk around the other as it smiles."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596151617686994954/image0.gif",
            "A baby elephant runs into the eager arms of a young man crouching on the ground. He hugs the elephant, beaming."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596151957014446102/image0.gif",
            "A woman is petting a baby elephant when it falls into her lap. She embraces it, face lighting up with happiness as she pets its belly."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596152610860433418/image0.gif",
            "Two adult elephants entwine their trunks together until their baby frolics between them."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596152963135700992/image0.gif",
            "A baby elephant tries to climb into the lap of a woman who looks as if she’s petting the most adorable thing in the world. She hugs its head for a second before they slip."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596153493815820289/image0.gif",
            "A baby elephant climbs on a laughing man from behind. He grabs the elephants trunk and shakes it in a friendly way."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596153871282470968/image0.gif",
            "A standing lion embraces a man in slow motion, its mane blowing in the wind."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596160280283840512/image0.gif",
            "A cat pets the side of a pig’s face as they embrace while lying down."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/596160482717597716/image0.gif",
            "Two cartoon cows embrace, blinking happily.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 15761808)


def pillage(person):
    """Inspiration and gif contributions from Dorea"""
    quote = "%s is on a pillaging spree!!! %s" % (person, VIKING * 3)
    gif_to_caption = [
        ("https://medievalkarl.files.wordpress.com/2015/02/7vh0ndg.gif",
            "A couple stand, peacefully framed by a stone window with vines. They scream when suddenly, the vikings charge."),
        ("https://www.eclectech.co.uk/b3ta/vikingbunny.gif",
            "A rabbit viking pillages a lawn by eating the grass."),
        ("https://66.media.tumblr.com/3ad6158c2bae0cf726539d6974ed6d5a/tumblr_o8s37xqzTF1tdy0nco1_500.gif",
            "Vikings cheer in front of a flaming wreckage."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569555567685664775/viking_battlefield.gif",
            "Vikings fight on an open field."),
        ("https://cdn.discordapp.com/attachments/539932855845781530/569556428092866648/viking_woman_strikes.gif",
            "A viking woman strikes down a man in front of her ship.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 13632027)


def cheer(cheerleader, mentions, text):
    victim = get_mention(mentions, text, "Friend")
    quote = "%s: You are being cheered on by %s!!!" % (victim, cheerleader)
    if victim in ["<@542048148776943657>", "Stufflebot", cheerleader]:
        quote = "%s: Stufflebot cheers you on too! :heart:" % cheerleader

    gif_to_caption = [
        ("https://cdn.discordapp.com/attachments/592480821890514944/602356893188489219/image0.gif",
            "A real cat in a cheer costume wiggles two oversized pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602381128887697429/image0.gif",
            "Snoopy dances back and forth while waving pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602381353635414027/image0.gif",
            "A big rabbit waves pink pom-poms over head next to a chick waving a flag."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602381860508794900/image0.gif",
            "A cartoon cat dances with pom-poms, it’s whiskers twitching to its movements."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602382148732977163/image0.gif",
            "A giant cartoon bunny hops from foot to foot on a stump, waving bushes like pom-poms. Flowers fly up in the background."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602382863131738122/image0.gif",
            "A very happy pikachu cheers with pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602383132800319518/image0.gif",
            "A Care Bear dances with rainbow tassels."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602383356092612621/image0.gif",
            "A cartoon bunny alternates high kicks while a cute white animal hops into view from behind it, throwing confetti."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602384163558916126/image0.gif",
            "A cactus with a flower on its head, punches its hands up in an alternating fashion, hitting two big “GO!”s."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602384583891222529/image0.gif",
            "A smiling cartoon cat with closed eyes dances side to side, its tail swishing with it. A heart pulses above its head."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602385048481824768/image0.gif",
            "A happy cartoon cat jumps into the air, cheering you on with yellow pom-poms and twitching ears."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602385384198111262/image0.gif",
            "“Cheerleader chibird” , a yellow blob with pom-poms says “hey! You got this! You’re doing great! Woo! Finish today strong!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602513976500420628/image0.gif",
            "A serious looking cartoon bear sways while pumping their pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602514272702169098/image0.gif",
            "Rowlet waves pom-poms nearly as big as itself around enthusiastically."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602514596934320138/image0.gif",
            "A cartoon panda waves pom-poms amidst confetti."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602515107762929664/image0.gif",
            "Hello Kitty in a bear costume cheers “GO! GO!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602515459090153472/image0.gif",
            "A derpy looking chicken dances enthusiastically with pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602515700380336129/image0.gif",
            "A happy mushroom runs, then jumps into the air cheerfully."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602516117683961876/image0.gif",
            "A small cartoon bunny dances with pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602516281115017217/image0.gif",
            "Three cartoon animals and a cartoon heart dance in formation with pom-poms."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602516489433513997/image0.gif",
            "A happy cartoon fox jumps into the air saying “yeah!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602516661152776221/image0.gif",
            "Five cartoon cats in a precarious pyramid formation wave happily."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602517286569377804/image0.gif",
            "Two bears dance back and forth, switching places while waving pom-poms in the air with confetti flying off them."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602517557898903552/image0.gif",
            "A smiling Patrick (from Spongebob) waves a flag and foam hand."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602517770923671573/image0.gif",
            "Hello Kitty waves two flags while marching in place among confetti."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602518034300796938/image0.gif",
            "Hello kitty turns to face you, winking and with two thumbs up, while saying “Yes! Yes!”"),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602518271043829790/image0.gif",
            "A real kitten standing on its hind legs dances back and forth with pom-poms in a heavily edited way."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602518679695130645/image0.gif",
            "A big bunny waves pom-poms up and down, dancing to the beat of floating musical notes."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602518987770691584/image0.gif",
            "A stoic cartoon cat steps back and forth while holding pom-poms over their head."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602519167257542676/image0.gif",
            "A cartoon panda jumps into the air. As it lands, more pandas appear behind it. They all jump in formation, and more identical pandas spawn in the background."),
        ("https://cdn.discordapp.com/attachments/592480821890514944/602519690891362337/image0.gif",
            "A happy shiba claps pom-poms together, then raises one.")
    ]
    return get_random_embed_same_quote(quote, gif_to_caption, 10507492)
