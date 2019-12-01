import discord


async def on_message_edit_pins(before, after):
    print("in message edit")
    # message is unpinned
    if before.pinned and not after.pinned:
        reactions = after.reactions
        # check if pin react by digmabot in there
    # message is pinned
    if not before.pinned and after.pinned:
        await after.add_reaction(":pushpin:")
    return


def populate_pins():
    # stuffle only command
    return
