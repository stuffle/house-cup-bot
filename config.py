from constants import *


"""
{
    serverID: {
        config: {

        },
        data: {
            voting: {}
        }
    }
}

COS/Red Writing Hood only things:
-House Cup Stuff
-Mod scan function
-Help for these functions
-Winnings
-Unwelcome
-Clearchannels
-Imprison
-Kink, whenshouldtheyfuck
"""

COS_SERVERS = [COS_GUILD_ID, RED_GUILD_ID]
COS_EXCLUSIVE = [
    "join", "leave", "actuallyleave", "time",
    "log", "daily", "post", "art", "beta", "comment",
    "workshop", "exercise", "comment", "wc", "excred", "remove",
    "points", "housepoints", "leaderboard", "standings",
    "sneak",
    "award", "deduct", "pingeveryone", "winnings",
    "startmonitoring", "stopmonitoring", "showmonitoring",
    "unwelcome", "clearchannels", "showimprisoned", "imprison",
    "caption", "captionshame"]

CSUA_SERVERS = [CSUA_GUILD_ID, TEST_GUILD_ID]
CSUA_PUBLIC_CHANNELS = [CSUA_WELCOME_CHANNEL_ID]
CSUA_EXCLUSIVE = ["whois", "identify"]