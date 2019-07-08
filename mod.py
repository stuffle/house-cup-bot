def mod_message(text, mention, channel_id):

    # Do not allow spoiler tags outside of spoilers
    if text.count("||") >= 2 and channel_id != "553216475708522506":
        return "Hey %s, we don't allow the usage of spoiler tags outside of #spoilers due to their inaccessibility with screen readers. Please remove them from your message. Thanks!" % mention

    return ""
