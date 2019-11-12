
# Discord Guild IDs
COS_GUILD_ID = 426319059009798146
RED_GUILD_ID = 497039992401428498
TEST_GUILD_ID = 539932855845781524
HP_FEMSLASH = 603458383999139881


# Discord Channel IDs
# COS Channel IDs
ART_CHANNEL = 426319343283077121
ART_DISCUSSION = 467386861845872660
BOT_SPAM = 426322538944266240
BULLETIN_BOARD = 549219513204342788
CHALLENGE_TIME = 428836873880993792
FEEL_GOOD = 595247070793826386
HALL_MONITORS = 623578046313660436
GAMING = 430731775267045386
MOD_MINUTES = 529117296371957760
MOD_PINGS = 602950953926393869
NSFW = 553213851827437609
NSFW_ART = 467410183723679745
NSFW_ART_DISCUSSION = 538509608604663808
NSFW_SHITPOSTING = 553215141379047434
SANITY_CHECKING = 603211515625209857
SFW_FLUFF = 480142773228666880
SHITPOSTING = 553214742702063636
SHOP_TALK = 619646538108370964
SNAP_SNAP = 595247137898627082
SPOILERS_CHANNEL_ID = 553216475708522506
TEA_AND_HUGS = 595247008340508683
TIME_CAPSULE = 496791619895558166

# Writing Hood Channel IDs
HOUSE_CUP = 507738193337122840
HOUSE_CUP_BOT = 553382529521025037
MOD_CHAT = 516733520542957568

# Test Server Channel IDs
GENERAL_IN_TEST = 539932855845781530
IMAGES_TEST = 592480821890514944
TODO = 587121361164435460


# Discord User IDs
STUFFLE_ID = 438450978690433024
STUFFLEBOT_ID = 542048148776943657

# Discord Mappings
SERVER_ID_TO_CHANNEL = {
    RED_GUILD_ID: HOUSE_CUP_BOT,
    TEST_GUILD_ID: GENERAL_IN_TEST,
    COS_GUILD_ID: BOT_SPAM
}
SERVER_ID_TO_CHANNEL_ANNOUNCE = {
    RED_GUILD_ID: HOUSE_CUP,
    COS_GUILD_ID: BULLETIN_BOARD
}


# Houses
SLYTHERIN = "slytherin"
RAVENCLAW = "ravenclaw"
GRYFFINDOR = "gryffindor"
HUFFLEPUFF = "hufflepuff"
HOUSES = [SLYTHERIN, GRYFFINDOR, RAVENCLAW, HUFFLEPUFF]
HOUSE_TO_EMOJI = {
    SLYTHERIN: ":snake:",
    RAVENCLAW: ":eagle:",
    GRYFFINDOR: ":lion:",
    HUFFLEPUFF: "🦡"
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

# House Cup Points
DAILY = "daily"
POST = "post"
BETA = "beta"
WORKSHOP = "workshop"
COMMENT = "comment"
EXCRED = "excred"
MOD_ADJUST = "mod_adjust"
WC = "wc"
ART = "art"
CATEGORIES = [DAILY, POST, BETA, ART, WORKSHOP,
              COMMENT, WC, EXCRED, MOD_ADJUST]
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
    ART: ":art:",
    COMMENT: ":keyboard:",
    WORKSHOP: ":sweat_smile:",
    EXCRED: ":star2:",
    MOD_ADJUST: ":innocent:",
    WC: ":chart_with_upwards_trend:",
    "word_count": ":books:"
}


### Custom Emoji ###

# Hearts
RAINBOW_HEART_500 = "<:rainbow_heart_500:609054991734538242>"
RAINBOW_HEART_100 = "<:rainbow_heart_100:609054831671508994>"
RAINBOW_HEART_50 = "<:rainbow_heart_50:609054469459804180>"
RAINBOW_HEART_10 = "<:rainbow_heart_10:609049620814888990>"
RAINBOW_HEART_5 = "<:rainbow_heart_5:609048811754618903>"
HEART_INFINITY = "<:infinity_heart:609126361759481882>"
HEART_777 = "<:777_heart:609123183395864586>"
HEART_666 = "<:666_heart:609113277175300103>"
HEART_420 = "<:420_heart:609065627025539085>"
HEART_69 = "<:69_heart:609056473355386880>"

# COS
VIKING = "<:dorea:507673373933961216>"

# Custom
YOU_TRIED_EMOJI = "<:you_tried:618116015930474506>"
WAT_EMOJI = "<:wat:625001102156496906>"
