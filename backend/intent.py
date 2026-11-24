import re


def detect_intent(text):

    text = text.lower().strip()

    words = re.findall(r"\b\w+\b", text)

    if any(word in text for word in [
        "cancel",
        "delete",
        "remove"
    ]):
        return "cancel_appointment"

    elif any(word in text for word in [
        "change",
        "reschedule",
        "move",
        "shift",
        "update"
    ]):
        return "reschedule_appointment"

    elif any(word in words for word in [
        "show",
        "view",
        "see"
    ]) and any(word in words for word in [
        "appointment",
        "appointments"
    ]):
        return "view_appointments"

    elif (
        "available" in words
        and any(word in words for word in [
            "doctor",
            "doctors",
            "specialist",
            "specialists"
        ])
    ):
        return "available_doctors"

    elif "appointment" in words:
        return "book_appointment"

    elif "weather" in words:
        return "weather"

    elif "time" in words:
        return "time"

    elif any(word in words for word in [
        "hello",
        "hi",
        "hey"
    ]):
        return "greeting"

    elif any(word in words for word in [
        "bye",
        "exit",
        "quit",
        "stop"
    ]):
        return "exit"

    return None