conversation = []


def add_message(sender, text):

    if not text:
        return

    conversation.append({
        "id": len(conversation) + 1,
        "sender": sender,
        "text": text
    })


def get_transcript():

    return conversation


def clear_transcript():

    conversation.clear()