import re
from datetime import datetime


def extract_time(text):

    text = text.lower().strip()

    text = text.replace("a.m.", "am")
    text = text.replace("p.m.", "pm")
    text = text.replace("a.m", "am")
    text = text.replace("p.m", "pm")

    # Convert 10.30 -> 10:30
    text = re.sub(
        r"(\d{1,2})\.(\d{2})",
        r"\1:\2",
        text
    )

    match = re.search(
        r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b",
        text
    )

    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    period = match.group(3)

    if period is None:

        if 1 <= hour <= 7:
            period = "pm"
        else:
            period = "am"

    if period == "pm" and hour != 12:
        hour += 12

    if period == "am" and hour == 12:
        hour = 0

    try:

        time_obj = datetime.strptime(
            f"{hour:02d}:{minute:02d}",
            "%H:%M"
        )

        return time_obj.strftime("%I:%M %p")

    except:

        return None